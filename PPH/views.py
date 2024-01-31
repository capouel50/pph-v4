import logging
import decimal
import os
import re
import time
from datetime import date

import jwt
import pandas as pd
import pdfplumber
from dj_rest_auth.registration.views import RegisterView
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.db.models import Count, Sum
from django.db.models.functions import ExtractWeek, ExtractYear, ExtractMonth
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.utils.encoding import force_bytes, force_str
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadTimeSignature
from rest_framework import generics
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.views import TokenObtainPairView

from PPH.serializers import (
    CustomRegisterSerializer, UserFunctionSerializer, SupplierSerializer, CustomUserSerializer,
    ContactSerializer, TypeMatiereSerializer, TypePrepSerializer, UniteMesureSerializer,
    FormeReadSerializer, FormeWriteSerializer, MatierePremiereReadSerializer, MatierePremiereWriteSerializer,
    FormuleSerializer, CompositionSerializer,
    CatalogueSerializer, VoieSerializer, ListeSerializer, ParametresPrepSerializer, ParametresFormulesSerializer,
    DemandesSerializer, FichesSerializer, ServiceSerializer, ParametresFormulesListSerializer,
    ConditionnementSerializer, CategorieMatiereSerializer, CatalogueImportSerializer
)
from .models import CustomUser, Supplier, UserFunction, Contact, \
    TypeMatiere, UniteMesure, Forme, MatierePremiere, TypePrep, \
    Formule, Composition, Catalogue, Liste, Voie, ParametresPrep, \
    ParametresFormules, Demandes, Fiches, Service, Conditionnement, CategorieMatiere, CatalogueImport

logger = logging.getLogger(__name__)

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            access_token = response.data['access']
            refresh_token = response.data['refresh']

            max_age_access = 60 * 60  # 1 heure en secondes
            max_age_refresh = 24 * 60 * 60  # 1 jour en secondes

            new_response = JsonResponse({'detail': 'Authentification réussie'})
            if settings.DEBUG:
                # En mode développement
                new_response.set_cookie('access_token', access_token, max_age=max_age_access, httponly=True,
                                        samesite='None', secure=True)
                new_response.set_cookie('refresh_token', refresh_token, max_age=max_age_refresh, httponly=True,
                                        samesite='None', secure=True)
            else:
                # En production
                new_response.set_cookie('access_token', access_token, max_age=max_age_access, httponly=True,
                                        samesite='None', secure=True)
                new_response.set_cookie('refresh_token', refresh_token, max_age=max_age_refresh, httponly=True,
                                        samesite='None', secure=True)

            return new_response

        return response


class CustomRegisterView(RegisterView):
    serializer_class = CustomRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        # Prepare data for the 'create' endpoint
        response_data = serializer.validated_data
        response_data["user"] = {
            "pk": user.pk,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name
        }

        token = Token.objects.create(user=user)

        # Générer un token pour le nouvel utilisateur
        email_token = default_token_generator.make_token(user)

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        domain = get_current_site(request).domain
        domain = domain.replace('http://', '').replace('https://', '')
        protocol = 'https' if request.is_secure() else 'http'
        activate_url = f'{protocol}://{domain}{reverse("validate_account", args=[uid, email_token])}'

        # Créer le contenu du mail de confirmation
        mail_subject = 'Confirmation de votre inscription.'
        message = render_to_string('account/email/email_confirmation_signup.html', {
            'user': user,
            'domain': get_current_site(request).domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': email_token,
            'activate_url': activate_url,
            'username' : user.username,
        })

        # Créer un message en texte brut pour les clients de messagerie qui ne supportent pas HTML
        plain_message = strip_tags(message)

        # Envoyer le mail de bienvenue
        send_mail(mail_subject, plain_message, settings.DEFAULT_FROM_EMAIL, [user.email], html_message=message)

        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)

@api_view(['GET'])
def confirm_email(request, token):
    serializer = URLSafeTimedSerializer(settings.SECRET_KEY)

    try:
        email = serializer.loads(token, salt='email-confirmation', max_age=3600)
    except (SignatureExpired, BadTimeSignature):
        return Response({'message': 'Le lien de confirmation est invalide ou est expiré.'}, status=400)

    user = CustomUser.objects.get(email=email)
    user.is_confirmed = True
    user.save()

    return Response({'message': 'Votre inscription est confirmée'})


class ValidateAccountView(APIView):
    def get(self, request, *args, **kwargs):
        uidb64 = kwargs.get('uidb64')
        token = kwargs.get('token')

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)

            if default_token_generator.check_token(user, token):
                user.is_active = True
                user.save()

                login_url = f"{settings.FRONTEND_DOMAIN}/login?accountActivated=true"
                return HttpResponseRedirect(login_url)

            else:
                return Response({"message": "Clé de validation invalide."}, status=400)

        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            return Response({"message": "Id utilisateur invalide."}, status=400)


@api_view(['POST'])
def logout(request):
    try:
        # Utilisez la demande pour identifier l'utilisateur
        user = request.user

        # Supprimez le token d'actualisation pour cet utilisateur
        # (cette logique peut varier en fonction de la façon dont vous stockez et gérez les tokens)
        OutstandingToken.objects.filter(user=user).delete()

        # Supprimez le cookie côté serveur (si vous l'utilisez)
        response = Response({"message": "Vous êtes déconnecté"}, status=status.HTTP_200_OK)
        response.delete_cookie("refreshToken")
        return response

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CustomUserListCreateView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

class CustomUserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        jwt_token = request.COOKIES.get('access_token')

        try:
            # Valider le token et obtenir sa date d'expiration
            UntypedToken(jwt_token)  # Valide le token
            token_data = jwt.decode(jwt_token, settings.SECRET_KEY, algorithms=["HS256"])
            expiry = token_data.get('exp')  # Date d'expiration du token en timestamp

            # Calculez le temps restant jusqu'à l'expiration (en secondes)
            time_remaining = expiry - int(time.time())

        except (InvalidToken, TokenError):
            time_remaining = 0  # ou toute autre valeur pour indiquer un token invalide

        data = {
            'id': user.id,
            'email': user.email,
            'firstName': user.first_name,
            'lastName': user.last_name,
            'userName': user.username,
            'function': user.function.title if user.function else None,
            'tokenExpiry': time_remaining
        }

        return Response(data)


class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer

    def create(self, request, *args, **kwargs):
        # Créez une instance de serializer en utilisant les données soumises par le formulaire
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        name = serializer.validated_data.get('name')
        if name:
            serializer.validated_data['name'] = name.capitalize()

        # Sauvegarder l'objet Supplier en base de données
        serializer.save()

        # Répondre avec les données du fournisseur créé et le code de statut 201 (Created)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class UserFunctionListCreateView(APIView):
    def get(self, request, *args, **kwargs):
        user_functions = UserFunction.objects.all()
        serializer = UserFunctionSerializer(user_functions, many=True)
        return Response(serializer.data)


class ContactView(generics.CreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        name = request.data.get("name")
        email = request.data.get("email")
        message = request.data.get("message")

        # Envoi du courrier
        subject = f"Message de {name}"
        send_mail(subject, message, email, [settings.DEFAULT_TO_EMAIL])

        return Response({"success": "Message envoyé avec succès"}, status=status.HTTP_201_CREATED)

class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
class DemandesViewSet(viewsets.ModelViewSet):
    queryset = Demandes.objects.all()
    serializer_class = DemandesSerializer

class TypeMatiereViewSet(viewsets.ModelViewSet):
    queryset = TypeMatiere.objects.all()
    serializer_class = TypeMatiereSerializer

class TypePrepViewSet(viewsets.ModelViewSet):
    queryset = TypePrep.objects.all()
    serializer_class = TypePrepSerializer

class ParametresPrepViewSet(viewsets.ModelViewSet):
    queryset = ParametresPrep.objects.all()
    serializer_class = ParametresPrepSerializer

class ParametresFormulesViewSet(viewsets.ModelViewSet):
    queryset = ParametresFormules.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT']:
            return ParametresFormulesListSerializer
        return ParametresFormulesSerializer

class UniteMesureViewSet(viewsets.ModelViewSet):
    queryset = UniteMesure.objects.all()
    serializer_class = UniteMesureSerializer

class ListeViewSet(viewsets.ModelViewSet):
    queryset = Liste.objects.all()
    serializer_class = ListeSerializer

class VoieViewSet(viewsets.ModelViewSet):
    queryset = Voie.objects.all()
    serializer_class = VoieSerializer

class ConditionnementViewSet(viewsets.ModelViewSet):
    queryset = Conditionnement.objects.all()
    serializer_class = ConditionnementSerializer

class CategorieMatiereViewSet(viewsets.ModelViewSet):
    queryset = CategorieMatiere.objects.all()
    serializer_class = CategorieMatiereSerializer

class FormeViewSet(viewsets.ModelViewSet):
    queryset = Forme.objects.all()
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return FormeReadSerializer
        return FormeWriteSerializer

class FichesViewSet(viewsets.ModelViewSet):
    queryset = Fiches.objects.all()
    serializer_class = FichesSerializer

    @action(detail=False, methods=['get'])
    def count_per_service(self, request):
        # Regroupement des fiches par service et comptage
        count = Fiches.objects.values('service').annotate(count=Count('id')).order_by('service')
        return Response(count)

    @action(detail=False, methods=['get'])
    def top_fiches_annuelles(self, request):
        current_year = timezone.now().year
        previous_year = current_year - 1

        # Récupération des 5 fiches les plus utilisées cette année
        top_current_year = (Fiches.objects.filter(date_fab__year=current_year)
                            .select_related('prep')  # Joindre la table Formule
                            .values('prep', 'prep__nom')  # Inclure le champ 'nom' de Formule
                            .annotate(count=Count('prep'))
                            .order_by('-count')[:5])

        # Récupération des données correspondantes pour l'année précédente
        top_previous_year = (
            Fiches.objects.filter(date_fab__year=previous_year, prep__in=[fiche['prep'] for fiche in top_current_year])
            .select_related('prep')  # Joindre la table Formule
            .values('prep', 'prep__nom')  # Inclure le champ 'nom' de Formule
            .annotate(count=Count('prep')))

        # Mise en forme des données pour la réponse
        response_data = {
            'current_year': list(top_current_year),
            'previous_year': {fiche['prep__nom']: fiche for fiche in top_previous_year}
        }

        return Response(response_data)

class FichesSemaine(APIView):
    def get(self, request, format=None):
        current_year = date.today().year
        fiches = Fiches.objects.annotate(week=ExtractWeek('date_fab'), year=ExtractYear('date_fab')).filter(year=current_year).values('week').annotate(count=Count('id'), qte=Sum('qté')).order_by('week')
        return Response(fiches)

class FichesMois(APIView):
    def get(self, request, format=None):
        current_year = date.today().year
        fiches = Fiches.objects.annotate(month=ExtractMonth('date_fab'), year=ExtractYear('date_fab')).filter(year=current_year).values('month').annotate(count=Count('id'), qte=Sum('qté')).order_by('month')
        return Response(fiches)

class MatierePremiereViewSet(viewsets.ModelViewSet):
    queryset = MatierePremiere.objects.all()

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return MatierePremiereReadSerializer
        return MatierePremiereWriteSerializer

    def retrieve_details(self, request, pk=None):
        matiere = self.get_object()
        serializer = self.get_serializer(matiere)
        return Response(serializer.data)

class FormuleViewSet(viewsets.ModelViewSet):
    queryset = Formule.objects.all()
    serializer_class = FormuleSerializer

    @action(detail=False, methods=['get'])
    def dernier_id(self, request):
        dernier_id = Formule.objects.latest('id').id
        return Response({'dernierId': dernier_id})

class CompositionViewSet(viewsets.ModelViewSet):
    queryset = Composition.objects.all()
    serializer_class = CompositionSerializer

    def create(self, request, *args, **kwargs):
        try:
            compositions_data = request.data.get('compositions', [])
            # Log the received data for debugging purposes
            logger.info(f'Received data: {compositions_data}')

            # Assume you are using a serializer for Composition
            serializer = CompositionSerializer(data=compositions_data, many=True)
            if serializer.is_valid():
                serializer.save()
                # Log the saved data for debugging purposes
                logger.info(f'Saved data: {serializer.data}')
                return Response(serializer.data, status=201)
            else:
                return Response(serializer.errors, status=400)
        except Exception as e:
            logger.error(f'Error processing composition creation: {str(e)}')
            return Response({'error': str(e)}, status=500)

class CompositionFilterView(APIView):
    def get(self, request, num_formule):
        compositions = Composition.objects.filter(num_formule=num_formule)
        serializer = CompositionSerializer(compositions, many=True)
        return Response(serializer.data)

class CatalogueImportViewSet(viewsets.ModelViewSet):
    queryset = CatalogueImport.objects.all()
    serializer_class = CatalogueImportSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Appelez extract_data_from_pdf pour traiter le nouvel enregistrement
        self.extract_data_from_pdf(sender=None, instance=serializer.instance, created=True)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # Appelez extract_data_from_pdf pour traiter la mise à jour de l'enregistrement
        self.extract_data_from_pdf(sender=None, instance=serializer.instance, created=False)

        return Response(serializer.data)
    def extract_data_from_pdf(self, sender, instance, created, **kwargs):
        print("Appel de la fonction")
        fournisseur = "Cooper"
        categories_script = ["Alcools & Alcoolats", "Chimiques & Excipients"]
        notifs = []
        statut_mapping = {
            "A": TypeMatiere.objects.get(id=5),  # Assurez-vous que l'ID correspond au bon TypeMatiere
            "CA": TypeMatiere.objects.get(id=4),
            "SA": TypeMatiere.objects.get(id=1),
            "E": TypeMatiere.objects.get(id=2),
            "T": TypeMatiere.objects.get(id=6),
            "C": TypeMatiere.objects.get(id=7)
        }

        try:
            # Vérifiez si les données du modèle correspondent aux critères du script
            if (instance.fournisseur.name.lower() == fournisseur.lower() and
                    instance.categorie.nom in categories_script and
                    instance.pdf.path and
                    instance.page_debut and
                    instance.page_fin and
                    instance.code_debut and
                    instance.code_fin):

                # Spécifiez le chemin vers le PDF en utilisant le chemin du fichier du modèle
                pdf_path = instance.pdf.path

                # Utilisez les données du modèle pour spécifier la plage de pages et les codes
                start_page = instance.page_debut
                end_page = instance.page_fin
                start_code = instance.code_debut
                end_code = instance.code_fin
                print('Paramètres entrés')

                # Obtenez le chemin absolu du répertoire de sauvegarde
                save_dir = os.path.join(settings.MEDIA_ROOT, 'catalogues')

                # Créez le chemin absolu du fichier CSV
                csv_filename = os.path.join(save_dir, f"catalogue_{fournisseur.lower()}.csv")

                # Assurez-vous que le répertoire existe, s'il n'existe pas, créez-le
                os.makedirs(save_dir, exist_ok=True)

                notifs.append({
                    'message': "Initialisation du traitement",
                    'type': 'info'
                })

                start_extraction = False

                # Ouvrez le PDF avec pdfplumber
                with pdfplumber.open(pdf_path) as pdf:
                    # Parcourez les pages dans la plage spécifiée
                    global_data = []

                    for page_number in range(start_page - 1, min(end_page, len(pdf.pages))):

                        print(f"Page en cours de traitement : {page_number + 1}")
                        data = []  # Réinitialisez la liste data pour chaque page
                        notifs.append({
                            'message': f'Traitement de la page {page_number + 1}',
                            'type': 'info'
                        })

                        page = pdf.pages[page_number]

                        # Extrait le texte de la page
                        page_text = page.extract_text()

                        # Divisez le texte en lignes
                        lines = page_text.split('\n')

                        # Initialisez la variable de sauvegarde de la ligne précédente pour la colonne "DESIGNATION"
                        prev_designation = ""

                        # Parcourez chaque ligne et essayez d'extraire les données selon les règles spécifiées
                        for line in lines:
                            # Vérifiez si la ligne commence par le format du code CPF
                            if re.match(r'^\d{1,3}(\s\d{3}){2}', line):
                                # Utilisez des expressions régulières pour extraire les données
                                match_cpf = re.search(r'(\d{1,3}(\s\d{3}){2})', line)
                                match_ean = re.search(r'\b\d{13}\b', line)
                                match_division = re.search(r'(\b\d{1,4}\s*[MLGK]+)\b', line)
                                match_puht = re.search(r'(\d+,\d+)\s*€$', line)
                                match_statut = re.search(r'\b(A|C|E|CA|SA|T)\b', line)
                                match_cmr = re.search(r'IMAGE|HEXAGONE', line, re.IGNORECASE)

                                # Examinez le texte pour détecter la présence du caractère "Â"
                                has_special_character = "Â" in line

                                # Examinez le texte pour détecter la présence du caractère "Â"
                                if "Â" in line:
                                    match_designation = re.search(r'Â(.*?)\b\d+\b', line)
                                elif match_ean:
                                    # Si "Â" n'est pas présent, commencez la désignation après le dernier chiffre du code EAN
                                    match_designation = re.search(rf'{match_ean.group(0)}(.*?)\b\d+\b', line)
                                else:
                                    match_designation = None

                                # Extrayez les données en fonction des correspondances
                                code_cpf = match_cpf.group(0) if match_cpf else ""
                                code_ean = match_ean.group(0) if match_ean else ""
                                division = match_division.group(0) if match_division else ""
                                puht = match_puht.group(1) if match_puht else ""
                                statut = match_statut.group(0) if match_statut else ""

                                # Marquez la colonne "CMR" comme "OUI" si le texte contient le caractère "Â"
                                if has_special_character or (match_cmr and match_cmr.group(0).upper() == "HEXAGONE"):
                                    cmr = True
                                else:
                                    cmr = False

                                # Extrait la désignation entre le dernier "Â" ou le dernier chiffre de la colonne "CODE EAN"
                                match_designation = match_designation.group(1).strip() if match_designation else ""

                                # Si la colonne "DESIGNATION" est vide, utilisez la valeur de la ligne précédente
                                if not match_designation:
                                    match_designation = prev_designation

                                # Mettez à jour la valeur de la ligne précédente pour la colonne "DESIGNATION"
                                prev_designation = match_designation

                                if "%" in line:
                                    # Utilisez une expression régulière pour capturer le chiffre précédent le caractère "%"
                                    match_percentage = re.search(r'(\d+)\s*%', line)
                                    if match_percentage:
                                        # Ajoutez le chiffre et le caractère '%' à la désignation
                                        percentage_value = match_percentage.group(1)
                                        match_designation += f" {percentage_value}%"

                                # Séparez la quantité et l'unité de la colonne "DIVISION" en deux colonnes distinctes
                                if match_division:
                                    division_parts = re.findall(r'(\d+)\s*([MLGK]+)', match_division.group(0))
                                    if division_parts:
                                        quantity = "".join([part[0] for part in division_parts])
                                        unit = "".join([part[1] for part in division_parts])
                                        # Transformez l'unité "k" en "kg" en ignorant la casse
                                        unit = "kg" if unit.lower() == "k" else unit
                                    else:
                                        quantity = ""
                                        unit = ""
                                else:
                                    quantity = ""
                                    unit = ""

                                match_puht = re.search(r'(\d+(?:\s\d{3})*(?:,\d+)?)\s*€$', line)
                                if match_puht:
                                    # Obtenez la correspondance du groupe de capture
                                    puht_match = match_puht.group(1)

                                    # Supprimez les espaces de la correspondance du prix
                                    puht_match = puht_match.replace(' ', '')

                                    # Remplacez la virgule par un point pour le format décimal
                                    puht_match = puht_match.replace(',', '.')

                                    # Convertissez le résultat en décimal
                                    puht_decimal = decimal.Decimal(puht_match)
                                else:
                                    puht_decimal = None

                                statut = match_statut.group(0) if match_statut else ""

                                # Transformez le statut en utilisant le dictionnaire de correspondance
                                statut_formatted = statut_mapping.get(statut, None)

                                # Vérifiez si nous avons atteint la ligne de début
                                if code_cpf == start_code:
                                    start_extraction = True  # Commencez à extraire les données à partir de ce point

                                # Vérifiez si nous avons atteint la ligne de fin
                                if code_cpf == end_code:
                                    data.append(
                                        [code_cpf, code_ean, cmr, match_designation, quantity, unit, statut_formatted,
                                         puht_decimal])
                                    start_extraction = False  # Arrêtez l'extraction des données

                                # Si nous sommes dans la plage de codes et que nous devons extraire les données, ajoutez-les à la liste data
                                if start_extraction:
                                    data.append(
                                        [code_cpf, code_ean, cmr, match_designation, quantity, unit, statut_formatted,
                                         puht_decimal])


                        # Une fois toutes les données extraites de la page, ajoutez-les à la liste globale data
                        global_data.extend(data)

                    # Créez un DataFrame pandas avec les données et les entêtes de colonnes appropriées
                    columns = ["CODE CPF", "CODE EAN", "CMR", "DESIGNATION", "QUANTITE", "UNITE", "STATUT", "P.U.H.T."]
                    df = pd.DataFrame(global_data, columns=columns)

                    print('Ajout des données')
                    notifs.append({
                        'message': "Ajout des données au préparatoire",
                        'type': 'info'
                    })

                    for row in global_data:
                        code_cpf, code_ean, cmr, designation, quantity, unit, statut_formatted, puht_decimal = row
                        designation = designation.capitalize()
                        catalogue = Catalogue(
                            designation=designation,
                            code_fournisseur=code_cpf,
                            cip=code_ean,
                            fournisseur=instance.fournisseur,
                            qté=quantity,
                            unite=unit.lower(),
                            type=statut_formatted,
                            prix=puht_decimal if puht_decimal else None,  # Handle cases where puht is empty
                            cmr=cmr,
                            categorie=instance.categorie
                            # You can set other fields accordingly
                        )
                        catalogue.save()

                notifs.append({
                    'message': "Catalogue importé",
                    'type': 'success'
                })

                print("Notifications ajoutées à la liste :")
                for notif in notifs:
                    print(notif)

        except Exception as e:
            # Gérez l'erreur ici, par exemple, en enregistrant les détails de l'erreur dans un journal
            print(f"Une erreur s'est produite lors de l'extraction des données depuis le PDF : {str(e)}")

            notifs.append({
                'message': f"Une erreur s'est produite lors de l'extraction des données depuis le PDF : {str(e)}",
                'type': 'error'
            })

        response_data = {
            'notifications': notifs,
            # Autres données de réponse
        }
        return JsonResponse(response_data)


class CatalogueViewSet(viewsets.ModelViewSet):
    queryset = Catalogue.objects.all()
    serializer_class = CatalogueSerializer



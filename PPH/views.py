from dj_rest_auth.registration.views import RegisterView
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadTimeSignature
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, action
from PPH.serializers import (
    CustomRegisterSerializer, UserFunctionSerializer, SupplierSerializer, CustomUserSerializer,
    ContactSerializer, TypeMatiereSerializer, TypePrepSerializer, UniteMesureSerializer,
    FormeSerializer, MatierePremiereSerializer, FormuleSerializer, CompositionSerializer,
    CatalogueSerializer, VoieSerializer, ListeSerializer, ParametresPrepSerializer, ParametresFormulesSerializer
)
from rest_framework_simplejwt.views import TokenObtainPairView
from django.http import JsonResponse, HttpResponseRedirect
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.conf import settings
import jwt
import time
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
from rest_framework import viewsets
from .models import CustomUser, Supplier, UserFunction, Contact,\
    TypeMatiere, UniteMesure, Forme, MatierePremiere, TypePrep, \
    Formule, Composition, Catalogue, Liste, Voie, ParametresPrep, ParametresFormules
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
import logging
from django.shortcuts import render

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
    serializer_class = ParametresFormulesSerializer

class UniteMesureViewSet(viewsets.ModelViewSet):
    queryset = UniteMesure.objects.all()
    serializer_class = UniteMesureSerializer

class ListeViewSet(viewsets.ModelViewSet):
    queryset = Liste.objects.all()
    serializer_class = ListeSerializer

class VoieViewSet(viewsets.ModelViewSet):
    queryset = Voie.objects.all()
    serializer_class = VoieSerializer

class FormeViewSet(viewsets.ModelViewSet):
    queryset = Forme.objects.all()
    serializer_class = FormeSerializer

class MatierePremiereViewSet(viewsets.ModelViewSet):
    queryset = MatierePremiere.objects.all()
    serializer_class = MatierePremiereSerializer

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

class CatalogueViewSet(viewsets.ModelViewSet):
    queryset = Catalogue.objects.all()
    serializer_class = CatalogueSerializer



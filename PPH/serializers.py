from dj_rest_auth.registration.serializers import RegisterSerializer
from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import CustomUser, Supplier, UserFunction, Contact, \
    TypeMatiere, UniteMesure, Forme, MatierePremiere, TypePrep, Formule, \
    Composition, Catalogue, Voie, Liste, ParametresPrep, ParametresFormules, \
    Demandes, Fiches, Service, Conditionnement, CategorieMatiere, CatalogueImport, \
    Reception, Etablissement, ParametresDemandes, ParametresFiches, Epi, EpiFormules, \
    Balances, FabricantsBalances, InstructionsBalances
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class CustomRegisterSerializer(RegisterSerializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()

    def custom_signup(self, request, user):
        user.first_name = self.validated_data.get('first_name').capitalize()
        user.last_name = self.validated_data.get('last_name').capitalize()
        user.username = (self.validated_data.get('first_name')[0] + self.validated_data.get('last_name')).lower()
        user.save()

    def get_cleaned_data(self):
        super(CustomRegisterSerializer, self).get_cleaned_data()

        return {
            'username': (self.validated_data.get('first_name')[0] + self.validated_data.get('last_name')).lower(),
            'password1': self.validated_data.get('password1'),
            'password2': self.validated_data.get('password2'),
            'email': self.validated_data.get('email'),
            'first_name': self.validated_data.get('first_name').capitalize(),
            'last_name': self.validated_data.get('last_name').capitalize(),
        }


class UserRegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')

    def create(self, validated_data):
        password1 = validated_data.get('password1')
        password2 = validated_data.get('password2')

        if password1 != password2:
            raise serializers.ValidationError({"password": "Les deux mots de passe ne correspondent pas"})

        user = CustomUser.objects.create_user(
            email=validated_data.get('email'),
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            password=password1
        )

        return user

class UserFunctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFunction
        fields = ['id', 'title', 'logo']

    def get_logo_url(self, obj):
        if obj.logo:
            return self.context['request'].build_absolute_uri(settings.MEDIA_URL + obj.logo.name)
        else:
            return None

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")


class CustomUserSerializer(serializers.ModelSerializer):
    function = UserFunctionSerializer()

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'function', 'is_staff', 'is_active']

class EtablissementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Etablissement
        fields = '__all__'

    def get_logo_url(self, obj):
        if obj.logo:
            return self.context['request'].build_absolute_uri(settings.MEDIA_URL + obj.logo.name)
        else:
            return None

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'

    def get_logo_url(self, obj):
        if obj.logo:
            return self.context['request'].build_absolute_uri(settings.MEDIA_URL + obj.logo.name)
        else:
            return None


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'name', 'email', 'message', 'created_at']


class ContactCreateView(APIView):
    def post(self, request):
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'
class TypeMatiereSerializer(serializers.ModelSerializer):

    class Meta:
        model = TypeMatiere
        fields = '__all__'


class UniteMesureSerializer(serializers.ModelSerializer):
    class Meta:
        model = UniteMesure
        fields = '__all__'

class ConditionnementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conditionnement
        fields = '__all__'

class CategorieMatiereSerializer(serializers.ModelSerializer):
    fournisseur = SupplierSerializer()
    class Meta:
        model = CategorieMatiere
        fields = '__all__'

class FormeReadSerializer(serializers.ModelSerializer):
    unite_mesure = UniteMesureSerializer()
    unite_stock = UniteMesureSerializer()
    class Meta:
        model = Forme
        fields = '__all__'

class FormeWriteSerializer(serializers.ModelSerializer):
    unite_mesure = UniteMesureSerializer
    unite_stock = UniteMesureSerializer
    class Meta:
        model = Forme
        fields = '__all__'

class ListeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Liste
        fields = '__all__'

class VoieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voie
        fields = '__all__'

class TypePrepSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypePrep
        fields = '__all__'

class ParametresPrepSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParametresPrep
        fields = '__all__'

class ParametresFormulesWriteSerializer(serializers.ModelSerializer):
    parametre = serializers.PrimaryKeyRelatedField(queryset=ParametresPrep.objects.all())

    class Meta:
        model = ParametresFormules
        fields = '__all__'
class ParametresFormulesListSerializer(serializers.ListSerializer):
    child = ParametresFormulesWriteSerializer()

    def create(self, validated_data):
        parametres_formules = [ParametresFormules(**item) for item in validated_data]
        return ParametresFormules.objects.bulk_create(parametres_formules)
class ParametresFormulesReadSerializer(serializers.ModelSerializer):
    parametre = ParametresPrepSerializer()
    class Meta:
        model = ParametresFormules
        fields = '__all__'

class ParametresDemandesReadSerializer(serializers.ModelSerializer):
    parametre = ParametresPrepSerializer()

    class Meta:
        model = ParametresDemandes
        fields = '__all__'

class ParametresDemandesWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParametresDemandes
        fields = ['num_demande', 'parametre', 'valeur_parametre']

    def create(self, validated_data):
        num_demande = validated_data.pop('num_demande')
        parametres_demande = ParametresDemandes.objects.create(num_demande=num_demande, **validated_data)
        return parametres_demande

class ParametresFichesReadSerializer(serializers.ModelSerializer):
    parametre = ParametresPrepSerializer()

    class Meta:
        model = ParametresFiches
        fields = '__all__'

class ParametresFichesWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParametresFiches
        fields = ['num_fiche', 'parametre', 'valeur_parametre']

    def create(self, validated_data):
        num_fiche = validated_data.pop('num_fiche')
        parametres_fiche = ParametresFiches.objects.create(num_fiche=num_fiche, **validated_data)
        return parametres_fiche

class MatierePremiereReadSerializer(serializers.ModelSerializer):
    type = TypeMatiereSerializer()
    forme = FormeReadSerializer()
    fournisseur = SupplierSerializer()
    cdt = ConditionnementSerializer()
    liste = ListeSerializer()
    unite_mesure = UniteMesureSerializer()

    class Meta:
        model = MatierePremiere
        fields = '__all__'

class MatierePremiereWriteSerializer(serializers.ModelSerializer):
    type = TypeMatiereSerializer
    forme = FormeReadSerializer
    fournisseur = SupplierSerializer
    cdt = ConditionnementSerializer
    liste = ListeSerializer
    unite_mesure = UniteMesureSerializer

    class Meta:
        model = MatierePremiere
        fields = '__all__'

class FormuleSerializer(serializers.ModelSerializer):
    type = TypePrepSerializer(read_only=True)
    liste = ListeSerializer(read_only=True)
    voie = VoieSerializer(read_only=True)
    class Meta:
        model = Formule
        fields = '__all__'

class CompositionWriteSerializer(serializers.ModelSerializer):
    matiere = MatierePremiereWriteSerializer
    class Meta:
        model = Composition
        fields = '__all__'

class CompositionReadSerializer(serializers.ModelSerializer):
    matiere = MatierePremiereReadSerializer()
    class Meta:
        model = Composition
        fields = '__all__'

class CatalogueImportSerializer(serializers.ModelSerializer):
    fournisseur = SupplierSerializer
    categorie = CategorieMatiereSerializer
    class Meta:
        model = CatalogueImport
        fields = '__all__'

    def get_pdf_url(self, obj):
        if obj.pdf:
            return self.context['request'].build_absolute_uri(settings.MEDIA_URL + obj.pdf.name)
        else:
            return None

class CatalogueSerializer(serializers.ModelSerializer):
    fournisseur = SupplierSerializer()
    class Meta:
        model = Catalogue
        fields = '__all__'

class DemandesReadSerializer(serializers.ModelSerializer):
    prep = FormuleSerializer()
    service = ServiceSerializer()
    class Meta:
        model = Demandes
        fields = '__all__'

class DemandesWriteSerializer(serializers.ModelSerializer):
    prep = FormuleSerializer
    service = ServiceSerializer
    class Meta:
        model = Demandes
        fields = '__all__'

class FichesReadSerializer(serializers.ModelSerializer):
    prep = FormuleSerializer()
    service = ServiceSerializer()
    class Meta:
        model = Fiches
        fields = '__all__'

class FichesWriteSerializer(serializers.ModelSerializer):
    prep = FormuleSerializer
    service = ServiceSerializer
    class Meta:
        model = Fiches
        fields = '__all__'

class BalancesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Balances
        fields = '__all__'

class InstructionsBalancesSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstructionsBalances
        fields = '__all__'

class EpiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Epi
        fields = '__all__'
class EpiFormulesReadSerializer(serializers.ModelSerializer):
    epi = EpiSerializer()
    class Meta:
        model = EpiFormules
        fields = '__all__'

class EpiFormulesWriteSerializer(serializers.ModelSerializer):
    epi = EpiSerializer
    class Meta:
        model = EpiFormules
        fields = '__all__'
class ReceptionWriteSerializer(serializers.ModelSerializer):
    matiere = MatierePremiereReadSerializer
    class Meta:
        model = Reception
        fields = '__all__'

class ReceptionReadSerializer(serializers.ModelSerializer):
    matiere = MatierePremiereReadSerializer()
    class Meta:
        model = Reception
        fields = '__all__'
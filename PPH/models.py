from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.urls import reverse
from datetime import date
from decimal import Decimal
from .utils import convert_quantity

class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        if not email:
            raise ValueError('L\'email est obligatoire')

        email = self.normalize_email(email)

        # Capitaliser les prénoms et les noms
        first_name = first_name.title()
        last_name = last_name.title()

        # Générer le username à partir de la première lettre du first_name et du last_name
        username = f'{first_name[0]}{last_name}'.lower().replace(' ', '_')

        user = self.model(username=username, email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, first_name, last_name, password=None):
        user = self.create_user(email, first_name, last_name, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class UserFunction(models.Model):
    title = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='users/', default='users/user.png')

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    function = models.ForeignKey(UserFunction, on_delete=models.SET_NULL, default=9, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    class Meta:
        ordering = ['last_name']

    def __str__(self):
        return self.username
class Supplier(models.Model):
    """
    Cet objet représente un fournisseur.
    """

    name = models.CharField(max_length=100, unique=True)
    address = models.CharField(max_length=100, blank=True)
    postal = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=254, blank=True)
    site = models.URLField(max_length=200, blank=True)
    user_code = models.CharField(max_length=100, blank=True)
    password = models.CharField(max_length=100, blank=True)
    logo = models.ImageField(upload_to='suppliers/', default='suppliers/usine.png')
    is_activate = models.BooleanField(default=True)
    download_catalogue = models.BooleanField(default=False)

    class Meta:
        ordering = ['name']

    def get_absolute_url(self):
        return reverse('fiche', args=[str(self.id)])

    def __str__(self):
        return self.name

class CategorieMatiere(models.Model):
    nom = models.CharField(max_length=200)
    fournisseur = models.ForeignKey(Supplier, on_delete=models.CASCADE)

    class Meta:
        ordering = ['nom']
    def __str__(self):
        return self.nom
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Service(models.Model):
    nom = models.CharField(max_length=200, null=True)
    def __str__(self):
        return str(self.nom)

class TypeMatiere(models.Model):
    nom = models.CharField(max_length=200)

    def __str__(self):
        return self.nom

class UniteMesure(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

class Conditionnement(models.Model):
    nom = models.CharField(max_length=100)

class Forme(models.Model):
    nom = models.CharField(max_length=200)
    unite_mesure = models.ForeignKey(UniteMesure, on_delete=models.CASCADE, related_name='formes_mesure')
    unite_stock = models.ForeignKey(UniteMesure, on_delete=models.CASCADE, related_name='formes_stock')

    def __str__(self):
        return self.nom

class Liste(models.Model):
    nom = models.CharField(max_length=200)

    def __str__(self):
        return self.nom

class Voie(models.Model):
    nom = models.CharField(max_length=200)

    def __str__(self):
        return self.nom

class TypePrep(models.Model):
    nom = models.CharField(max_length=200)

    def __str__(self):
        return self.nom

class ParametresPrep(models.Model):
    nom = models.CharField(max_length=200)
    unite = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.nom

class ParametresFormules(models.Model):
    num_formule = models.CharField(max_length=200)
    parametre = models.ForeignKey(ParametresPrep, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.num_formule} - {self.parametre}"

class MatierePremiere(models.Model):
    nom = models.CharField(max_length=200, null=True)
    type = models.ForeignKey(TypeMatiere, on_delete=models.CASCADE, default=1, null=False)
    forme = models.ForeignKey(Forme, on_delete=models.CASCADE, null=True)
    cdt = models.ForeignKey(Conditionnement, on_delete=models.CASCADE, null=True)
    qté_cdt = models.DecimalField(max_digits=10, decimal_places=2)
    unite_cdt = models.CharField(max_length=200, null=True)
    fournisseur = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    code_fournisseur = models.CharField(max_length=200, null=True)
    ean = models.CharField(max_length=200, null=True)
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    prix_unit = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    qté_stock = models.PositiveIntegerField(null=True, blank=True)
    stock_mini = models.PositiveIntegerField()
    liste = models.ForeignKey(Liste, on_delete=models.CASCADE, null=True)
    stockee = models.BooleanField(default=False)
    cde_auto = models.BooleanField(default=False)
    cde = models.BooleanField(default=False)
    attente_livraison = models.BooleanField(default=False)
    cmr = models.BooleanField(default=False)
    froid = models.BooleanField(default=False)
    unite_mesure = models.ForeignKey(UniteMesure, on_delete=models.CASCADE, null=True)

    def save(self, *args, **kwargs):
        if self.prix and self.qté_cdt and self.unite_cdt and self.unite_mesure:
            try:
                # Convertissez la quantité du conditionnement à l'unité de mesure
                qté_unite_mesure = convert_quantity(
                    self.qté_cdt, self.unite_cdt.lower(), self.unite_mesure.nom
                )
                # Calculez le prix unitaire
                self.prix_unit = self.prix / qté_unite_mesure
            except ValueError:
                # Gérez le cas où la conversion n'est pas possible
                self.prix_unit = None
        else:
            self.prix_unit = None
        super(MatierePremiere, self).save(*args, **kwargs)


class Formule(models.Model):
    nom = models.CharField(max_length=200, null=False)
    type = models.ForeignKey(TypePrep, on_delete=models.CASCADE, default=1, null=False)
    liste = models.ForeignKey(Liste, on_delete=models.CASCADE, default=1, null=False)
    voie = models.ForeignKey(Voie, on_delete=models.CASCADE, default=1, null=False)
    duree = models.CharField(max_length=200, null=False)
    froid = models.BooleanField(default=False)
    lumiere = models.BooleanField(default=False)
    agiter = models.BooleanField(default=False)
    mode_operatoire = models.CharField(max_length=1000, null=False)
    contre_indications = models.CharField(max_length=1000, null=False)
    publications = models.CharField(max_length=1000, null=True)

    class Meta:
        ordering = ['nom']

    def __str__(self):
        return self.nom

class Composition(models.Model):
    num_formule = models.CharField(max_length=200, null=True)
    matiere = models.ForeignKey(MatierePremiere, on_delete=models.CASCADE, null=True)
    qté = models.CharField(max_length=200, null=True)
    unite = models.ForeignKey(UniteMesure, on_delete=models.CASCADE, null=True)
    calcul = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.num_formule)

class CatalogueImport(models.Model):
    fournisseur = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    categorie = models.ForeignKey(CategorieMatiere, on_delete=models.CASCADE)
    page_debut = models.IntegerField()
    page_fin = models.IntegerField()
    code_debut = models.CharField(max_length=200)
    code_fin = models.CharField(max_length=200)
    date_import = models.DateTimeField(auto_now_add=True)
    pdf = models.FileField(upload_to='imports/')
    class Meta:
        ordering = ['date_import']
    def __str__(self):
        return str(self.date_import)
class Catalogue(models.Model):
    designation = models.CharField(max_length=200)
    code_fournisseur = models.CharField(max_length=200)
    cip = models.CharField(max_length=200)
    fournisseur = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    qté = models.DecimalField(max_digits=10, decimal_places=2)
    unite = models.CharField(max_length=200)
    prix = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    prix_unit = models.DecimalField(max_digits=10, decimal_places=2, editable=False, null=True)
    type = models.ForeignKey(TypeMatiere, on_delete=models.CASCADE, null=True)
    cmr = models.BooleanField(default=False)
    froid = models.BooleanField(default=False)
    categorie = models.ForeignKey(CategorieMatiere, on_delete=models.CASCADE, null=True)

    def save(self, *args, **kwargs):
        # S'assurer que prix et qté sont des Decimal
        prix_decimal = Decimal(self.prix)
        qté_decimal = Decimal(self.qté)

        # Calculer le prix unitaire seulement si qté est supérieure à zéro pour éviter la division par zéro
        if qté_decimal > 0:
            self.prix_unit = prix_decimal / qté_decimal
        else:
            self.prix_unit = Decimal('0.00')  # Ou une autre valeur par défaut si qté est zéro

        super(Catalogue, self).save(*args, **kwargs)


    class Meta:
        ordering = ['designation']

    def __str__(self):
        return self.designation

class Demandes(models.Model):
    prep = models.ForeignKey(Formule, on_delete=models.CASCADE, null=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True)
    qté = models.CharField(max_length=200, null=True)
    date_prevu = models.DateField(default=date.today, blank=True)
    commentaire = models.CharField(max_length=200, null=True)
    def __str__(self):
        return f"{self.prep} - {self.date_prevu}"

class Fiches(models.Model):
    prep = models.ForeignKey(Formule, on_delete=models.CASCADE, null=True)
    attente_controle = models.BooleanField(default=False)
    date_fab = models.DateField(default=date.today, blank=True)
    service = models.CharField(max_length=200, null=True)
    qté = models.CharField(max_length=200, null=True)
    def __str__(self):
        return str(self.prep)



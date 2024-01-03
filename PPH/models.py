from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.urls import reverse


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

    class Meta:
        ordering = ['name']

    def get_absolute_url(self):
        return reverse('fiche', args=[str(self.id)])

    def __str__(self):
        return self.name


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class TypeMatiere(models.Model):
    nom = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='matieres/', default='matieres/actif.jpg')

    def __str__(self):
        return self.nom

class UniteMesure(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

class Forme(models.Model):
    nom = models.CharField(max_length=200)
    unite_stock = models.CharField(max_length=200)
    unite_mesure = models.ForeignKey(UniteMesure, on_delete=models.CASCADE)

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
        return self.nom

class MatierePremiere(models.Model):
    nom = models.CharField(max_length=200)
    type = models.ForeignKey(TypeMatiere, on_delete=models.CASCADE, default=1, null=False)
    forme = models.ForeignKey(Forme, on_delete=models.CASCADE)
    qté_cdt = models.CharField(max_length=200)
    fournisseur = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    prix_unit = models.DecimalField(max_digits=10, decimal_places=2)
    qté_stock = models.PositiveIntegerField()
    stock_mini = models.PositiveIntegerField()
    liste = models.ForeignKey(Liste, on_delete=models.CASCADE)
    stockee = models.BooleanField(default=False)
    cde = models.BooleanField(default=False)

    class Meta:
        ordering = ['nom']

    def __str__(self):
        return self.nom


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

    def __str__(self):
        return str(self.num_formule)

class Catalogue(models.Model):
    designation = models.CharField(max_length=200)
    code_fournisseur = models.CharField(max_length=200)
    cip = models.CharField(max_length=200)
    fournisseur = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    qté = models.DecimalField(max_digits=10, decimal_places=2)
    unite = models.CharField(max_length=200)

    class Meta:
        ordering = ['designation']

    def __str__(self):
        return self.nom
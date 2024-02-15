from django.contrib import admin
from .models import CustomUser, UserFunction, Supplier, TypeMatiere, \
    UniteMesure, Forme, MatierePremiere, Liste, TypePrep, Formule, Composition, \
    Catalogue, Voie, ParametresPrep, ParametresFormules, Demandes, Fiches, Service, \
    Conditionnement, CategorieMatiere, CatalogueImport, Reception, Etablissement



class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'function', 'is_active', 'is_staff')
    search_fields = ('username', 'email')
    list_filter = ('is_active', 'is_staff', 'function')


class UserFunctionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    search_fields = ('title',)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserFunction, UserFunctionAdmin)
admin.site.register(Supplier)

@admin.register(Etablissement)
class EtablissementAdmin(admin.ModelAdmin):
    list_display = ['nom_long','nom_court', 'address', 'postal', 'city', 'phone', 'email', 'site', 'logo']
@admin.register(TypeMatiere)
class TypeMatiereAdmin(admin.ModelAdmin):
    list_display = ['id','nom']

@admin.register(UniteMesure)
class UniteMesureAdmin(admin.ModelAdmin):
    list_display = ['nom']

@admin.register(Forme)
class FormeAdmin(admin.ModelAdmin):
    list_display = ['nom', 'unite_mesure', 'unite_stock']

@admin.register(Liste)
class ListeAdmin(admin.ModelAdmin):
    list_display = ['nom']

@admin.register(Conditionnement)
class ConditionnementAdmin(admin.ModelAdmin):
    list_display = ['nom']
@admin.register(Voie)
class VoieAdmin(admin.ModelAdmin):
    list_display = ['nom']

@admin.register(TypePrep)
class TypePrepAdmin(admin.ModelAdmin):
    list_display = ['nom']

@admin.register(ParametresPrep)
class ParametresPrepAdmin(admin.ModelAdmin):
    list_display = ['nom', 'unite']

@admin.register(ParametresFormules)
class ParametresFormulesAdmin(admin.ModelAdmin):
    list_display = ['num_formule', 'parametre']

@admin.register(CategorieMatiere)
class CategorieMatiereAdmin(admin.ModelAdmin):
    list_display = ['nom', 'fournisseur']
@admin.register(Demandes)
class DemandesAdmin(admin.ModelAdmin):
    list_display = ['prep', 'qté', 'date_prevu']

@admin.register(Fiches)
class FichesAdmin(admin.ModelAdmin):
    list_display = ['prep']

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['nom']

@admin.register(MatierePremiere)
class MatierePremiereAdmin(admin.ModelAdmin):
    list_display = ['nom', 'type', 'forme', 'qté_cdt', 'fournisseur', 'prix', 'prix_unit',
                    'qté_stock', 'stock_mini', 'stockee', 'cde', 'cde_auto', 'attente_livraison',]

@admin.register(Formule)
class TypePrepAdmin(admin.ModelAdmin):
    list_display = ['nom', 'type']

@admin.register(Composition)
class Composition(admin.ModelAdmin):
    list_display = ['num_formule', 'matiere', 'qté', 'unite']

@admin.register(CatalogueImport)
class CatalogueImportAdmin(admin.ModelAdmin):
    list_display = ['pdf', 'fournisseur', 'categorie', 'page_debut', 'page_fin', 'code_debut', 'code_fin', 'date_import']

@admin.register(Catalogue)
class CatalogueAdmin(admin.ModelAdmin):
    list_display = ['designation', 'code_fournisseur', 'cip', 'fournisseur', 'qté', 'unite']

@admin.register(Reception)
class ReceptionAdmin(admin.ModelAdmin):
    list_display = ['date_reception', 'matiere', 'lot', 'peremption', 'qte', 'certificat']
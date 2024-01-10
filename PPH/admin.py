from django.contrib import admin
from .models import CustomUser, UserFunction, Supplier, TypeMatiere, \
    UniteMesure, Forme, MatierePremiere, Liste, TypePrep, Formule, Composition, \
    Catalogue, Voie, ParametresPrep, ParametresFormules, Demandes, Fiches


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

@admin.register(TypeMatiere)
class TypeMatiereAdmin(admin.ModelAdmin):
    list_display = ['id','nom','logo']

@admin.register(UniteMesure)
class UniteMesureAdmin(admin.ModelAdmin):
    list_display = ['nom']

@admin.register(Forme)
class FormeAdmin(admin.ModelAdmin):
    list_display = ['nom', 'unite_mesure', 'unite_stock']

@admin.register(Liste)
class ListeAdmin(admin.ModelAdmin):
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

@admin.register(Demandes)
class DemandesAdmin(admin.ModelAdmin):
    list_display = ['prep', 'qté']

@admin.register(Fiches)
class FichesAdmin(admin.ModelAdmin):
    list_display = ['prep']

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

@admin.register(Catalogue)
class CatalogueAdmin(admin.ModelAdmin):
    list_display = ['designation', 'code_fournisseur', 'cip', 'fournisseur', 'qté', 'unite']
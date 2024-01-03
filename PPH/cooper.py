import os
import django
import requests
from bs4 import BeautifulSoup
import csv
import re

# Configuration de l'environnement Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "your_project.settings")
django.setup()

from your_app.models import Catalogue, Supplier  # Importer le modèle et les modèles associés

# URL de la première page
url = "https://www.cooper.fr/hcl/produits?field_gamme_tid=2025&field_code_cooper_value=&field_code_value=&field_cip_acl_value=&title="

# Initialisation du lien de la page suivante
next_url = url

# Ouverture du fichier CSV (optionnel, seulement si vous voulez aussi sauvegarder dans un CSV)
with open('cooper_data.csv', mode='w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')

    while next_url:
        # Requête GET à la page
        response = requests.get(next_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extraction des données de la table
        # ... (le code pour l'extraction des données reste le même)

        for data in extracted_data:  # Supposons que 'extracted_data' est votre liste de données extraites
            # Création d'un nouvel objet Catalogue
            catalogue_entry = Catalogue(
                designation=data[2],  # Assurez-vous que l'ordre des données correspond
                code_fournisseur=data[0],
                cip=data[1],
                fournisseur=Supplier.objects.get_or_create(nom=data[3])[0],  # Exemple pour gérer le fournisseur
                qté=decimal.Decimal(data[4]),  # Convertir en Decimal
                unite=data[5]
            )
            catalogue_entry.save()

    # Extraction du lien de la page suivante
    # ... (le code pour extraire le lien de la page suivante reste le même)

# Fin du script


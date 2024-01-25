import pandas as pd
from PPH.models import Catalogue

# Chemin vers votre fichier Excel
excel_file_path = 'Cooper_pharma.xlsx'

# Lire les données du fichier Excel
df = pd.read_excel(excel_file_path)

df['Référence four.'] = df['Référence four.'].str.replace(' ', '')

# Itérer sur chaque ligne du DataFrame
for index, row in df.iterrows():
    code_fournisseur = row['Référence four.']
    prix = row['Prix']  # Assurez-vous que le nom de colonne 'prix' correspond à votre fichier Excel

    # Trouver et mettre à jour l'enregistrement dans le modèle Catalogue
    try:
        catalogue_item = Catalogue.objects.get(code_fournisseur=code_fournisseur)
        catalogue_item.prix = prix  # Assurez-vous que 'prix' est un champ dans votre modèle
        catalogue_item.save()
    except Catalogue.DoesNotExist:
        print(f"Aucun objet Catalogue trouvé pour le code fournisseur {code_fournisseur}")

print("Importation terminée.")

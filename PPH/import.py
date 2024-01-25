import csv
from decimal import Decimal, InvalidOperation
from PPH.models import Catalogue, Supplier

# Chemin du fichier CSV
csv_file_path = 'cooper_data_update.csv'

def create_catalogue_from_csv(file_path, fournisseur_id):
    with open(file_path, mode='r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            designation = row['Nom']
            code_fournisseur = row['Code Cooper']
            cip = row['CIP / ACL']
            qté_str = row['Quantité'].replace(',', '.')  # Remplacer la virgule par un point
            try:
                qté = Decimal(qté_str)  # Convertir en nombre décimal
            except InvalidOperation:
                print(f"Valeur invalide pour la quantité: {qté_str}")
                continue  # Passer à la ligne suivante en cas d'erreur
            unite = row['Unité']
            cdt = row['UCD']

            fournisseur = Supplier.objects.get(id=fournisseur_id)

            catalogue_item = Catalogue(
                designation=designation,
                code_fournisseur=code_fournisseur,
                cip=cip,
                fournisseur=fournisseur,
                qté=qté,
                unite=unite,
                cdt=cdt
            )
            catalogue_item.save()

fournisseur_id = 47

create_catalogue_from_csv(csv_file_path, fournisseur_id)



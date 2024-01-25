import csv
import re

# Chemin du fichier CSV original
input_csv_path = 'cooper_data.csv'

# Chemin du fichier CSV de sortie
output_csv_path = 'cooper_data_update.csv'

# Regex pour identifier la quantité et l'unité
# Cette regex prend en compte les formats où l'unité est avant ou après les chiffres.
quantity_regex = re.compile(
    r'(.*?)(\b[kKmgMGlL]+|\b[lLmM][Ll])?\s*(\d+[\.,]?\d*)\s*([kKmgMGlL]+|[lLmM][Ll])?\s*$'
)

# Ouvrir le fichier CSV original en lecture
with open(input_csv_path, mode='r', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    headers = next(reader)  # Assumer la première ligne comme en-tête

    # Ouvrir le fichier CSV de sortie en écriture
    with open(output_csv_path, mode='w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile, delimiter=',')

        # Ajouter deux nouvelles colonnes "Quantité" et "Unité" à l'en-tête
        new_headers = headers[:2] + ['Nom', 'Quantité', 'Unité'] + headers[3:]
        writer.writerow(new_headers)

        # Lecture de chaque ligne du fichier original
        for row in reader:
            designation = row[2]  # La désignation est supposée être dans la troisième colonne
            # Utilisation de regex pour séparer le nom, la quantité et l'unité
            match = quantity_regex.match(designation)
            if match:
                name = match.group(1).strip()
                unit_pre = match.group(2)
                quantity = match.group(3).strip()
                unit_post = match.group(4)

                # Déterminer quelle unité utiliser (pré ou post quantité)
                unit = unit_pre or unit_post
                unit = unit.strip() if unit else ''

                # Écriture dans le nouveau fichier avec les valeurs séparées
                writer.writerow(row[:2] + [name] + [quantity, unit] + row[3:])
            else:
                # Si le format ne correspond pas à la regex, écrire la ligne telle quelle
                writer.writerow(row[:2] + [designation] + ['', ''] + row[3:])






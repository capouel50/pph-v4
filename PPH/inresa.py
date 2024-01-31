import pdfplumber
import pandas as pd
import re

fournisseur = "Cooper"
categories_script = ["Alcools & Alcoolats", "Chimiques & Excipients"]
# Spécifiez le chemin vers votre PDF
pdf_path = ""

# Spécifiez la plage de pages à analyser
start_page = 7
end_page = 16
start_code = ""
end_code = ""

# Créez une liste pour stocker les données extraites
data = []

# Ouvrez le PDF avec pdfplumber
with pdfplumber.open(pdf_path) as pdf:
    # Parcourez les pages dans la plage spécifiée
    for page_number in range(start_page - 1, min(end_page, len(pdf.pages))):
        page = pdf.pages[page_number]

        # Extrait le texte de la page
        page_text = page.extract_text()

        # Divisez le texte en lignes
        lines = page_text.split('\n')

        # Initialisez la variable de sauvegarde de la ligne précédente pour la colonne "DESIGNATION"
        prev_designation = ""

        # Parcourez chaque ligne et essayez d'extraire les données selon les règles spécifiées
        for line in lines:
            # Vérifiez si la ligne commence par le format du code CPF
            if re.match(r'^\d{1,3}(\s\d{3}){2}', line):
                # Utilisez des expressions régulières pour extraire les données
                match_cpf = re.search(r'(\d{1,3}(\s\d{3}){2})', line)
                match_ean = re.search(r'\b\d{13}\b', line)
                match_division = re.search(r'(\b\d{1,4}\s*[MLGK]+)\b', line)
                match_puht = re.search(r'(\d+,\d+)\s*€$', line)
                match_statut = re.search(r'\b(A|C|E|CA|SA|T)\b', line)
                match_cmr = re.search(r'IMAGE|HEXAGONE', line, re.IGNORECASE)

                # Examinez le texte pour détecter la présence du caractère "Â"
                has_special_character = "Â" in line

                # Examinez le texte pour détecter la présence du caractère "Â"
                if "Â" in line:
                    match_designation = re.search(r'Â(.*?)\b\d+\b', line)
                elif match_ean:
                    # Si "Â" n'est pas présent, commencez la désignation après le dernier chiffre du code EAN
                    match_designation = re.search(rf'{match_ean.group(0)}(.*?)\b\d+\b', line)
                else:
                    match_designation = None

                # Extrayez les données en fonction des correspondances
                code_cpf = match_cpf.group(0) if match_cpf else ""
                code_ean = match_ean.group(0) if match_ean else ""
                division = match_division.group(0) if match_division else ""
                puht = match_puht.group(1) if match_puht else ""
                statut = match_statut.group(0) if match_statut else ""

                # Marquez la colonne "CMR" comme "OUI" si le texte contient le caractère "Â"
                if has_special_character or (match_cmr and match_cmr.group(0).upper() == "HEXAGONE"):
                    cmr = "OUI"
                else:
                    cmr = "NON"

                # Extrait la désignation entre le dernier "Â" ou le dernier chiffre de la colonne "CODE EAN"
                match_designation = match_designation.group(1).strip() if match_designation else ""

                # Si la colonne "DESIGNATION" est vide, utilisez la valeur de la ligne précédente
                if not match_designation:
                    match_designation = prev_designation

                # Mettez à jour la valeur de la ligne précédente pour la colonne "DESIGNATION"
                prev_designation = match_designation

                # Séparez la quantité et l'unité de la colonne "DIVISION" en deux colonnes distinctes
                if match_division:
                    division_parts = re.findall(r'(\d+)\s*([MLGK]+)', match_division.group(0))
                    if division_parts:
                        quantity = "".join([part[0] for part in division_parts])
                        unit = "".join([part[1] for part in division_parts])
                        # Transformez l'unité "k" en "kg" en ignorant la casse
                        unit = "kg" if unit.lower() == "k" else unit
                    else:
                        quantity = ""
                        unit = ""
                else:
                    quantity = ""
                    unit = ""

                # Ajoutez les données extraites à la liste
                data.append([code_cpf, code_ean, cmr, match_designation, quantity, unit, statut, puht])

# Créez un DataFrame pandas avec les données et les entêtes de colonnes appropriées
columns = ["CODE CPF", "CODE EAN", "CMR", "DESIGNATION", "QUANTITE", "UNITE", "STATUT", "P.U.H.T."]
df = pd.DataFrame(data, columns=columns)

csv_filename = f"catalogue_{fournisseur.lower()}.csv"
df.to_csv(csv_filename, index=False)

print(f"Données extraites et enregistrées dans {csv_filename}")

import decimal
import re
import traceback
from celery import shared_task
import pandas as pd
import pdfplumber
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

@shared_task
def send_extraction_notification(message, message_type="info"):
    notification = {
        "message": message,
        "notification_type": message_type  # Clé renommée pour différencier du 'type' pour Django Channels
    }
    print("Une notif")
    print(notification)

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "notifications_pph",  # Nom du groupe WebSocket
        {
            "type": "send_data_extraction_notification",  # Correspond au nom de la méthode dans votre consommateur
            "notification": notification  # Objet contenant le message et le type de notification
        }
    )


def extract_data_from_pdf(instance):
    from .models import TypeMatiere, Catalogue
    notifs = []
    send_extraction_notification.delay("Vérification des paramètres d'extraction.", message_type="info")
    fournisseur = "Cooper"
    categories_script = ["Alcools & Alcoolats", "Chimiques & Excipients"]
    categories_materiel = ["Flaconnage", "Gélules", "Matériel & Articles de conditionnement", "Pots"]
    statut_mapping = {
        "A": TypeMatiere.objects.get(id=5),
        "CA": TypeMatiere.objects.get(id=4),
        "SA": TypeMatiere.objects.get(id=1),
        "E": TypeMatiere.objects.get(id=2),
        "T": TypeMatiere.objects.get(id=6),
        "C": TypeMatiere.objects.get(id=7),
    }

    try:
        if (instance.fournisseur.name.lower() == fournisseur.lower() and
                instance.categorie and
                instance.pdf.path and
                instance.page_debut and
                instance.page_fin and
                instance.code_debut and
                instance.code_fin):

            pdf_path = instance.pdf.path
            start_page = instance.page_debut
            end_page = instance.page_fin
            start_code = instance.code_debut
            end_code = instance.code_fin

            start_extraction = False

            send_extraction_notification.delay("Analyse en cours.", message_type="info")

            with pdfplumber.open(pdf_path) as pdf:
                global_data = []

                for page_number in range(start_page - 1, min(end_page, len(pdf.pages))):

                    data = []
                    send_extraction_notification.delay(f'Traitement de la page {page_number + 1}', message_type="info")

                    page = pdf.pages[page_number]
                    page_text = page.extract_text()
                    lines = page_text.split('\n')
                    prev_designation = ""

                    for line in lines:
                        if re.match(r'^\d{1,3}(\s\d{3}){2}', line):

                            match_cpf = re.search(r'(\d{1,3}(\s\d{3}){2})', line)
                            match_ean = re.search(r'\b\d{13}\b', line)
                            match_division = re.search(r'(\b\d{1,4}\s*[MLGK]+)\b', line)
                            match_puht = re.search(r'(\d+,\d+)\s*€$', line)
                            match_statut = re.search(r'\b(A|C|E|CA|SA|T)\b', line)
                            match_cmr = re.search(r'IMAGE|HEXAGONE', line, re.IGNORECASE)

                            has_special_character = "Â" in line

                            if "Â" in line:
                                match_designation = re.search(r'Â(.*?)\b\d+\b', line)
                            elif match_ean:
                                match_designation = re.search(rf'{match_ean.group(0)}(.*?)\b\d+\b', line)
                            else:
                                match_designation = None

                            code_cpf = match_cpf.group(0) if match_cpf else ""
                            code_ean = match_ean.group(0) if match_ean else ""
                            division = match_division.group(0) if match_division else ""
                            puht = match_puht.group(1) if match_puht else ""
                            statut = match_statut.group(0) if match_statut else ""

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
                                cmr = True
                            else:
                                cmr = False

                            # Extrait la désignation entre le dernier "Â" ou le dernier chiffre de la colonne "CODE EAN"
                            match_designation = match_designation.group(1).strip() if match_designation else ""

                            # Si la colonne "DESIGNATION" est vide, utilisez la valeur de la ligne précédente
                            if not match_designation:
                                match_designation = prev_designation

                            # Mettez à jour la valeur de la ligne précédente pour la colonne "DESIGNATION"
                            prev_designation = match_designation

                            if "%" in line:
                                # Utilisez une expression régulière pour capturer le chiffre précédent le caractère "%"
                                match_percentage = re.search(r'(\d+)\s*%', line)
                                if match_percentage:
                                    # Ajoutez le chiffre et le caractère '%' à la désignation
                                    percentage_value = match_percentage.group(1)
                                    match_designation += f" {percentage_value}%"

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

                            match_puht = re.search(r'(\d+(?:\s\d{3})*(?:,\d+)?)\s*€$', line)
                            if match_puht:
                                # Obtenez la correspondance du groupe de capture
                                puht_match = match_puht.group(1)

                                # Supprimez les espaces de la correspondance du prix
                                puht_match = puht_match.replace(' ', '')

                                # Remplacez la virgule par un point pour le format décimal
                                puht_match = puht_match.replace(',', '.')

                                # Convertissez le résultat en décimal
                                puht_decimal = decimal.Decimal(puht_match)
                            else:
                                puht_decimal = None

                            statut = match_statut.group(0) if match_statut else ""

                            # Transformez le statut en utilisant le dictionnaire de correspondance
                            statut_formatted = statut_mapping.get(statut, None)

                            # Vérifiez si nous avons atteint la ligne de début
                            if code_cpf == start_code:
                                start_extraction = True
                                send_extraction_notification.delay(f"Code d'initialisation détecté : {start_code}", message_type="info")
                                # Commencez à extraire les données à partir de ce point

                            # Vérifiez si nous avons atteint la ligne de fin
                            if code_cpf == end_code:
                                send_extraction_notification.delay(f"Code d'arrêt détecté : {end_code}.", message_type="info")
                                data.append(
                                    [code_cpf, code_ean, cmr, match_designation, quantity, unit, statut_formatted,
                                     puht_decimal])
                                start_extraction = False  # Arrêtez l'extraction des données

                            # Si nous sommes dans la plage de codes et que nous devons extraire les données, ajoutez-les à la liste data
                            if start_extraction:
                                data.append(
                                    [code_cpf, code_ean, cmr, match_designation, quantity, unit, statut_formatted,
                                     puht_decimal])

                    # Une fois toutes les données extraites de la page, ajoutez-les à la liste globale data
                    global_data.extend(data)

                # Créez un DataFrame pandas avec les données et les entêtes de colonnes appropriées
                columns = ["CODE CPF", "CODE EAN", "CMR", "DESIGNATION", "QUANTITE", "UNITE", "STATUT", "P.U.H.T."]
                df = pd.DataFrame(global_data, columns=columns)

                send_extraction_notification.delay("Ajouts des données au préparatoire", message_type="info")

                for row in global_data:
                    code_cpf, code_ean, cmr, designation, quantity, unit, statut_formatted, puht_decimal = row
                    designation = designation.capitalize()
                    catalogue = Catalogue(
                        designation=designation,
                        code_fournisseur=code_cpf,
                        cip=code_ean,
                        fournisseur=instance.fournisseur,
                        qté=quantity,
                        unite=unit.lower(),
                        type=statut_formatted,
                        prix=puht_decimal if puht_decimal else None,  # Handle cases where puht is empty
                        cmr=cmr,
                        categorie=instance.categorie
                        # You can set other fields accordingly
                    )
                    catalogue.save()

            send_extraction_notification.delay("Catalogue importé", message_type="success")

    except Exception as e:
        traceback.print_exc()
        # Gérez l'erreur ici, par exemple, en enregistrant les détails de l'erreur dans un journal
        send_extraction_notification.delay(f"Une erreur s'est produite lors de l'extraction des données depuis le PDF : {str(e)}", message_type="error")

    return notifs


def convert_quantity(quantity, from_unit, to_unit):
    # Ajoutez ici la logique de conversion pour chaque unité
    conversion_rates = {
        'kg': {
            'kg': 1,
            'g': 1000,
            'mg': 1000000,
        },
        'g': {
            'kg': 0.001,
            'g': 1,
            'mg': 1000,
            'gttes': 55,
        },
        'mg': {
            'kg': 0.000001,
            'g': 0.001,
            'mg': 1,
        },
        'gttes': {
             'g': 0.018,
             'mg': 18,
        },
        'l': {
            'l': 1,
            'ml': 1000,
        },
        'ml': {
            'l': 0.001,
            'ml': 1,
        },
    }

    if from_unit in conversion_rates and to_unit in conversion_rates[from_unit]:
        conversion_rate = conversion_rates[from_unit][to_unit]
        converted_quantity = quantity * conversion_rate
        return converted_quantity
    else:
        # Gérez ici le cas où la conversion n'est pas possible
        raise ValueError("Conversion non supportée")


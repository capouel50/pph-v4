import requests
from bs4 import BeautifulSoup
import csv
import re

# définir l'URL de la première page
url = "https://www.cooper.fr/hcl/produits?field_gamme_tid=2025&field_code_cooper_value=&field_code_value=&field_cip_acl_value=&title="

# initialiser une variable pour stocker le lien de la page suivante
next_url = url

# ouvrir un fichier CSV pour écrire les données
with open('cooper_data.csv', mode='w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')

    while next_url:
        # effectuer une demande GET à la page
        response = requests.get(next_url)

        # analyser la page avec Beautiful Soup
        soup = BeautifulSoup(response.text, 'html.parser')

        # extraire les lignes de données de la table
        table = soup.find('table', {'class': 'views-table cols-9'})
        tbody = table.find('tbody')
        rows = tbody.find_all('tr')

        # extraire les en-têtes de colonnes si nécessaire
        if 'header_written' not in locals():
            header = [th.text.strip() for th in table.find('thead').find_all('th')]
            writer.writerow(header)
            header_written = True

        # extraire les données de chaque ligne
        for row in rows:
            cols = row.find_all('td')
            # formater les données de chaque colonne
            data = []
            for i, col in enumerate(cols):
                if i != header.index('Désignation'):
                    data.append(re.sub(
                        r'(?<=\d)(?=[a-zA-Z])|(?<=[a-zA-Z])(?=\d)',
                        ' ',
                        col.text.strip()
                    ).replace('"', '').lower())
                else:
                    words = col.text.strip().split()
                    last_word = words[-1]
                    # Vérification s'il y a des chiffres et / ou une lettre dans le dernier mot
                    if any(char.isdigit() for char in last_word) and any(char.isalpha() for char in last_word):
                        # Vérification s'il n'y a pas d'espace entre chiffres et lettres
                        if not any(char.isdigit() and words[-1][i + 1].isalpha() for i, char in enumerate(last_word) if
                                   char.isdigit()):
                            last_word_letters = ''.join(c for c in last_word if c.isalpha())
                            last_word_numbers = ''.join(c for c in last_word if c.isdigit())
                            words[-1] = f"{last_word_letters} {last_word_numbers}"
                        # Vérification si un espace doit être ajouté
                        elif not any(
                                char.isdigit() and words[-1][i + 1].isspace() for i, char in enumerate(last_word) if
                                char.isdigit()):
                            last_word_letters = ''.join(c for c in last_word if c.isalpha())
                            last_word_numbers = ''.join(c for c in last_word if c.isdigit())
                            words[-1] = f"{last_word_letters} {last_word_numbers}"
                    elif last_word.isalpha():
                        # S'il n'y a pas de chiffres et que le mot précédent n'en contient pas non plus, supprimer le dernier mot
                        if words[-2].isalpha():
                            words.pop()
                        else:
                            pass
                    # Vérification s'il s'agit d'un nombre
                    elif last_word.isdigit():
                        if i > 0:
                            # Inversion si le précédent n'est pas un nombre
                            if not words[-2].isdigit() and len(words) > 1:
                                words[-1], words[-2] = words[-2], words[-1]
                    data.append(' '.join(words).rstrip().replace('"', '').capitalize().replace('"', ''))
            data = [re.sub('\s{2,}', ' ', i) for i in
                    data]  # remplace toutes les occurrences de deux ou plusieurs espaces par un seul espace
            writer.writerow(data)

            # insérer les données dans la base de données


        # extraire le lien de la page suivante s'il existe
        pager_next = soup.find('li', {'class': 'pager__item pager__item--next'})
        if pager_next:
            next_url = "https://www.cooper.fr" + pager_next.find('a')['href']
        else:
            next_url = None



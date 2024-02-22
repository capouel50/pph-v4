import os
from setuptools import setup, find_packages

def update_setup():
    # Lire les dépendances depuis requirements.txt
    with open('requirements.txt', 'r') as req_file:
        requirements = req_file.readlines()

    # Filtrer la dépendance à exclure
    requirements = [req.strip() for req in requirements if 'twisted-iocpsupport' not in req]

    # Générer le nouveau contenu pour setup.py
    setup_content = """
from setuptools import setup, find_packages

setup(
    name='PPH',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
{}
    ],
)
""".format(',\n'.join(["        '{}',".format(req.strip()) for req in requirements]))

    # Écrire le nouveau contenu dans setup.py
    with open('setup.py', 'w') as setup_file:
        setup_file.write(setup_content)

if __name__ == '__main__':
    update_setup()


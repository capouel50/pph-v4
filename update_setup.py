import os

def update_setup_and_requirements():
    # Ouvrir le fichier setup.py en mode lecture
    with open("setup.py", "r") as setup_file:
        setup_lines = setup_file.readlines()

    # Ouvrir le fichier requirements.txt en mode lecture
    with open("requirements.txt", "r") as requirements_file:
        requirements_lines = requirements_file.readlines()

    # Trouver l'index où commencent les dépendances dans le fichier setup.py
    dependencies_index = None
    for i, line in enumerate(setup_lines):
        if "install_requires" in line:
            dependencies_index = i
            break

    # Si l'index des dépendances est trouvé dans setup.py
    if dependencies_index is not None:
        # Exécuter la commande 'pip freeze' pour obtenir les dépendances avec leurs versions
        pip_freeze_output = os.popen('pip freeze').read().strip().split('\n')

        # Créer une liste pour stocker les dépendances avec leurs versions
        dependencies_list = []
        for line in pip_freeze_output:
            package, version = line.split('==')
            dependencies_list.append(f'    "{package}=={version}"\n')

        # Reconstruire la ligne 'install_requires' dans setup.py avec les versions et des sauts de ligne
        new_dependencies_lines = ['install_requires=[\n'] + dependencies_list + ['],\n']

        # Remplacer l'ancienne ligne 'install_requires' par la nouvelle dans setup.py
        setup_lines[dependencies_index] = ''.join(new_dependencies_lines)

        # Réécrire le fichier setup.py avec les nouvelles dépendances
        with open("setup.py", "w") as setup_file:
            setup_file.writelines(setup_lines)

        print("Le fichier setup.py a été mis à jour avec succès.")

    else:
        print("Impossible de trouver l'index des dépendances dans le fichier setup.py.")

    # Écrire les dépendances dans requirements.txt
    with open("requirements.txt", "w") as requirements_file:
        for line in pip_freeze_output:
            requirements_file.write(line + '\n')

        print("Le fichier requirements.txt a été mis à jour avec succès.")

if __name__ == "__main__":
    update_setup_and_requirements()




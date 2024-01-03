# Utilisez une image de base
FROM python:3.8

# Définissez le répertoire de travail dans le conteneur
WORKDIR /app

# Copiez les fichiers nécessaires dans le conteneur
COPY requirements.txt .

# Installez les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copiez le reste des fichiers dans le conteneur
COPY . /app

# Exposez le port sur lequel l'application écoute
EXPOSE 8000

# Commande pour exécuter l'application lorsque le conteneur démarre
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

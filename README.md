# Epic Events

Epic Events est une application de gestion d'événements.

## Prérequis

- Python 3.x
- PostgreSQL
- SQLAlchemy
- Alembic

## Installation

### 1. Cloner le répertoire

Dans le terminal de commandes, entrez `git clone https://github.com/Clement-Mchar/Epic-Events`

Entrez `cd epic-events`

### 2. Configurer la base de données PostgreSQL

Créez une base de données nommée `epic_events` et un utilisateur `app_user` qui peut agir sur cette base de données.

Connectez-vous à PostgreSQL en utilisant psql :

Entrez `psql -U postgres`

Ensuite, exécutez les commandes SQL suivantes pour créer la base de données et l'utilisateur :


`CREATE USER app_user WITH PASSWORD 'your_password';`

`CREATE DATABASE epic_events OWNER app_user;`

`GRANT ALL PRIVILEGES ON DATABASE epic_events TO app_user;`

### 3. Créer un environnement virtuel

Entrez `python -m venv env`

Activez-le en entrant `env\scripts\activate` dans le terminal.

### 4. Installer les dépendances

Entrez `pip install -r requirements.txt`

### 5. Configurer les variables d'environnement

Créez un fichier `.env` à la racine du projet et ajoutez-y la ligne suivante avec les informations de connexion à votre base de données :

`DATABASE_URL=postgresql://app_user:your_password@localhost:5432/epic_events`

### 6. Ajouter la journalisation de Sentry

Créez un compte ou connectez-vous sur sentry.io, puis créez un projet et ajoutez l'adresse du projet aux variables d'environnements :

`DSN=https://id.ingest.de.sentry.io/project`

### 7. Lancer les migrations de la base de données

Entrez `alembic upgrade head`

Créez le dossier versions à l'intérieur du dossier migrations en entrant `mkdir -p migrations/versions`

Entrez `alembic revision --autogenerate -m "Initial migration"`

Importez sqlalchemy_utils dans le fichier de migration et supprimez la longueur du mot de passe

### 8. Créer les rôles

Entrez `python create_roles.py`

### 9. Créer un utilisateur (manager)

Entrez `python create_user.py`

Entrez le mot de passe de l'utilisateur

### 10. Connexion à l'application

Entrez `python main.py`

Entrez l'email et le mot de passe de l'utilisateur désiré

import os
from dotenv import load_dotenv

# Charger les variables du fichier .env
load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))
#load_dotenv()

class Config:

    # Récupérer les informations de connexion à la base de données depuis les variables d'environnement
    DB_TYPE = os.getenv("DB_TYPE")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")
    DATABASE_URL = f"{DB_TYPE}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}" # Créer l'URL de connexion à la base de données

    # Configurations générales
    DEBUG = os.getenv("DEBUG", "false").lower() in ("true", "1", "yes")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    # Ajoute d'autres paramètres si nécessaire
    NBA_API_TEMPO = int(os.getenv("NBA_API_TEMPO", 60))
    NBA_API_TEMPO_PLAYERS = int(os.getenv("NBA_API_TEMPO_PLAYERS", 100))

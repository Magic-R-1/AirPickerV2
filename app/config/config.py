import os
import logging
from dotenv import load_dotenv

# Charger les variables du fichier .env
load_dotenv()

class Config:

    # Récupérer les informations de connexion à la base de données depuis les variables d'environnement
    DB_TYPE = os.getenv("DB_TYPE")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")
    DATABASE_URL = f"{DB_TYPE}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}" # Créer l'URL de connexion à la base de données

    # Récupérer le logger spécifique à SQLAlchemy
    sqlalchemy_logger = logging.getLogger('sqlalchemy.engine')
    # Supprimer tous les handlers existants
    for handler in sqlalchemy_logger.handlers[:]:
        sqlalchemy_logger.removeHandler(handler)
    # Configurer le niveau de log de SQLAlchemy
    sqlalchemy_logger.setLevel(logging.WARNING)
    # Désactiver la propagation des logs SQLAlchemy
    sqlalchemy_logger.propagate = False

    # Configurer le logging global avec le niveau provenant du .env
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
    logging.basicConfig(level=LOG_LEVEL)

    # NBA API config
    NBA_API_TEMPO = int(os.getenv("NBA_API_TEMPO", 60))
    NBA_API_TEMPO_PLAYERS = int(os.getenv("NBA_API_TEMPO_PLAYERS", 100))
    SAISON_EN_COURS = int(os.getenv("SAISON_EN_COURS", 2024))

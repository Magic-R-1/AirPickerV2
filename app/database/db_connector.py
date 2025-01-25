from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from config.config import Config

# URL de connexion de la base de données
DATABASE_URL = Config.DATABASE_URL

# Création de l'engine SQLAlchemy
engine = create_engine(DATABASE_URL, echo=True)

# Sessionmaker pour créer des sessions de base de données
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@contextmanager
def session_scope():
    """ Fournit un gestionnaire de contexte pour la session SQLAlchemy. """
    # Créer une nouvelle session
    session = SessionLocal()
    try:
        yield session  # Retourne la session pour qu'elle soit utilisée dans le bloc
    finally:
        session.close()  # Assure que la session est fermée après utilisation

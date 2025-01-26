from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from app.config.config import Config
from sqlalchemy.ext.declarative import declarative_base

# Définir la base pour SQLAlchemy
Base = declarative_base()

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

def reset_metadata():
    # Réinitialiser les métadonnées avec une nouvelle instance
    metadata = MetaData()
    Base.metadata = metadata

if __name__ == "__main__":
    reset_metadata()
    print(Base.metadata.tables.keys())


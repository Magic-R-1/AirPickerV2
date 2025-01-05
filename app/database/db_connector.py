from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import Config


# Utiliser l'URL de connexion depuis la configuration centralisée
DATABASE_URL = Config.DATABASE_URL

# Création de l'engine SQLAlchemy
engine = create_engine(DATABASE_URL, echo=True)

# Déclaration de la base
Base = declarative_base()

# Sessionmaker pour créer des sessions de base de données
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
import time
from tqdm import tqdm

from app.config import Config
from app.database.db_connector import engine, SessionLocal
from app.models.boxscore import Boxscore


class BoxscoreTableLifeCycle:

    @staticmethod
    def create_boxscore_table():
        Boxscore.__table__.create(engine)

        print("Table 'boxscore' créée avec succès.")

    @staticmethod
    def fill_boxscore_table():
        print("toto")

    @staticmethod
    def clear_boxscore_table():
        with SessionLocal() as session:
            try:
                # Vider la table en supprimant tous les enregistrements
                session.query(Boxscore).delete()
                session.commit()  # Valider les changements
                print("La table boxscore a été vidée avec succès.")
            except Exception as e:
                session.rollback()  # Annuler en cas d'erreur
                print(f"Une erreur est survenue lors du vidage de la table boxscore : {e}")

    @staticmethod
    def drop_boxscore_table():
        with SessionLocal() as session:
            try:
                # Supprimer la table Boxscore
                Boxscore.__table__.drop(bind=session.get_bind())
                print("La table boxscore a été supprimée avec succès.")
            except Exception as e:
                print(f"Une erreur est survenue lors de la suppression de la table boxscore : {e}")
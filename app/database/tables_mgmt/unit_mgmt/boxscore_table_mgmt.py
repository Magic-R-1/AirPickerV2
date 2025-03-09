import re

from sqlalchemy.exc import IntegrityError
from tqdm import tqdm

from app.database.db_connector import engine, SessionLocal
from app.models.boxscore import Boxscore
from app.dao.teamgamelog_dao import TeamGameLogDAO
from app.services.boxscore_service import BoxscoreService
from app.services.nba_api_service import NbaApiService
from app.dao.boxscore_dao import BoxscoreDAO
from app.dao.player_dao import PlayerDAO


class BoxscoreTableMgmt:

    @staticmethod
    def create_boxscore_table():
        Boxscore.__table__.create(engine)
        print("Table 'boxscore' créée avec succès.")

    @staticmethod
    def fill_boxscore_table():
        BoxscoreTableMgmt.update_boxscore_table()

    @staticmethod
    # TODO : à enlever si update_boxscore_table OK
    def update_boxscore_table_old():
        liste_game_id_in_teamgamelog = set(TeamGameLogDAO.get_list_unique_game_ids())  # Convertir en set dès le début
        liste_game_id_in_boxscore = set(BoxscoreDAO.get_list_unique_game_ids())

        liste_nouveaux_game_id = liste_game_id_in_teamgamelog - liste_game_id_in_boxscore  # Set opération directe

        with SessionLocal() as db:
            try:
                # Parcourir les game_id
                for game_id in tqdm(
                        liste_nouveaux_game_id,
                        desc="Boucle sur les game_id",
                        unit="game_id",
                        total=len(liste_nouveaux_game_id)
                ):

                    # Obtenir le DF boxscore
                    df_boxscore = NbaApiService.get_boxscore_by_game_id(game_id)

                    # Mapper les données vers le modèle Boxscore
                    list_boxscore_sqlalchemy = BoxscoreService.map_boxscore_df_to_list_boxscore_model(df_boxscore)

                    if list_boxscore_sqlalchemy:
                        db.bulk_save_objects(list_boxscore_sqlalchemy)  # Insertion en batch

                # Augmenter l'indentation de un si nécessaire
                db.flush()
                db.commit()

            except Exception as e:
                db.rollback()
                print(f"Une erreur est survenue lors de l'ajout des boxscores : {e}")

    @staticmethod
    def update_boxscore_table():
        liste_game_id_in_teamgamelog = TeamGameLogDAO.get_list_unique_game_ids()
        liste_game_id_in_boxscore = BoxscoreDAO.get_list_unique_game_ids()
        liste_nouveaux_game_id = list(set(liste_game_id_in_teamgamelog) - set(liste_game_id_in_boxscore))

        with SessionLocal() as db:
            for game_id in tqdm(liste_nouveaux_game_id, desc="Boucle sur les game_id", unit="game_id", total=len(liste_nouveaux_game_id)):
                try:
                    df_boxscore = NbaApiService.get_boxscore_by_game_id(game_id)
                    list_boxscore_sqlalchemy = BoxscoreService.map_boxscore_df_to_list_boxscore_model(df_boxscore)

                    if list_boxscore_sqlalchemy:
                        db.bulk_save_objects(list_boxscore_sqlalchemy)
                        db.flush()
                        db.commit()

                except IntegrityError as e:
                    db.rollback()

                    # Extraction des player_id manquants
                    missing_players = set(re.findall(r"Key \(player_id\)=\((\d+)\)", str(e)))
                    if missing_players:
                        print(f"Joueurs manquants détectés : {missing_players}, tentative d'ajout...")

                        for player_id in missing_players:
                            PlayerDAO.add_player_from_player_id(int(player_id))

                        # Réessayer l'insertion après avoir ajouté les joueurs
                        try:
                            if list_boxscore_sqlalchemy:
                                db.bulk_save_objects(list_boxscore_sqlalchemy)
                                db.flush()
                                db.commit()
                        except IntegrityError as e:
                            db.rollback()
                            print(f"Échec de la réinsertion pour le game_id {game_id}: {e}")


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


if __name__ == "__main__":
    BoxscoreTableMgmt.fill_boxscore_table()
    print("")

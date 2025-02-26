from tqdm import tqdm

from app.database.db_connector import engine, SessionLocal
from app.models.boxscore import Boxscore
from app.dao.teamgamelog_dao import TeamGameLogDAO
from app.services.boxscore_service import BoxscoreService
from app.services.nba_api_service import NbaApiService
from app.services.team_service import TeamService


class BoxscoreTableMgmt:

    @staticmethod
    def create_boxscore_table():
        Boxscore.__table__.create(engine)
        print("Table 'boxscore' créée avec succès.")

    @staticmethod
    # TODO
    def fill_boxscore_table():
        # Récupérer la liste des ids de toutes les équipes dans la table team
        team_ids_list = TeamService.get_list_all_team_ids()

        # Boucler sur les joueurs pour ajouter leurs informations
        with SessionLocal() as db:
            try:
                # Parcourir les équipes
                for index, team_id in tqdm( # Ne pas oublier l'index, qui évite de créer des tuples
                        enumerate(team_ids_list),
                        desc="Boucle sur les équipes",
                        unit="équipe",
                        total=len(team_ids_list)
                ):

                    # Liste des game_id
                    liste_game_ids = TeamGameLogDAO.get_list_game_id_by_team_id(team_id)

                    # Parcourir les game_id
                    for i, game_id in tqdm( # Ne pas oublier l'index, qui évite de créer des tuples
                            enumerate(liste_game_ids),
                            desc="Boucle sur les game_id",
                            unit="game_id",
                            total=len(liste_game_ids)
                    ):

                        # Obtenir le DF boxscore
                        df_boxscore = NbaApiService.get_boxscore_by_game_id(game_id)

                        # Mapper les données vers le modèle Boxscore
                        list_boxscore_sqlalchemy = BoxscoreService.map_boxscore_df_to_boxscore_model(df_boxscore)

                        for boxscore_sqlalchemy in list_boxscore_sqlalchemy:
                            # Ajouter l'entrée à la session sans valider immédiatement
                            db.add(boxscore_sqlalchemy)

                db.commit()

            except Exception as e:
                db.rollback()
                print(f"Une erreur est survenue lors de l'ajout des boxscores : {e}")


    @staticmethod
    # TODO
    def update_boxscore_table():
        print("")

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
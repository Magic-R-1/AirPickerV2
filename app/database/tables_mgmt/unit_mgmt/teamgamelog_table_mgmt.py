import pandas as pd
from tqdm import tqdm

from app.database.db_connector import engine, SessionLocal
from app.models.teamgamelog import TeamGameLog
from app.services.team_service import TeamService
from app.services.teamgamelog_service import TeamGameLogService
from app.services.nba_api_service import NbaApiService


class TeamGameLogTableMgmt:

    @staticmethod
    def create_teamgamelog_table():
        TeamGameLog.__table__.create(engine)
        print("Table 'teamgamelog' créée avec succès.")

    @staticmethod
    def fill_teamgamelog_table():
        TeamGameLogTableMgmt.update_teamgamelog_table()

    @staticmethod
    def update_teamgamelog_table():
        # Récupérer la liste des ids de toutes les équipes dans la table team
        team_ids_list = TeamService.get_list_all_team_ids()

        # Boucle id d'équipe par id d'équipe
        with SessionLocal() as db:
            try:
                # Initialiser un compteur global pour les TeamGameLogs
                count_teamgamelogs = 0

                # Récupérer toute la table teamgamelog avant la boucle
                df_teamgamelog_in_base = TeamGameLogService.get_df_all_teamgamelogs()

                # Si aucun enregistrement existant, utiliser un DataFrame vide
                if df_teamgamelog_in_base is None or df_teamgamelog_in_base.empty:
                    print(
                        "Aucun TeamGameLog existant trouvé dans la base. Tous les enregistrements API seront considérés comme nouveaux.")
                    df_teamgamelog_in_base = pd.DataFrame(columns=["team_id", "game_id"])

                for team_id in tqdm(
                        team_ids_list,
                        desc="Parcourir les équipes",
                        unit="équipe",
                        total=len(team_ids_list)
                ):
                    # Filtrer les lignes de la table entière pour ne garder que celles correspondant à l'équipe en cours
                    df_current_team_teamgamelog_in_base = df_teamgamelog_in_base[
                        df_teamgamelog_in_base['team_id'] == team_id]

                    # Appel API à TeamGameLog, pour récupérer les TeamGameLogs de l'équipe
                    teamgamelog_df = NbaApiService.get_team_game_log_by_team_id(team_id)

                    # Ne conserver que les lignes pour lesquelles les valeurs de game_id ne sont pas en base
                    teamgamelog_df = teamgamelog_df[
                        ~teamgamelog_df["game_id"].isin(df_current_team_teamgamelog_in_base["game_id"])]

                    # Incrémenter le compteur global avec le nombre de nouvelles lignes
                    count_teamgamelogs += len(teamgamelog_df)

                    # Mapper les données vers le modèle Boxscore
                    list_teamgamelog_sqlalchemy = TeamGameLogService.map_df_teamgamelog_to_list_teamgamelog_model(
                        teamgamelog_df)

                    if list_teamgamelog_sqlalchemy:
                        db.bulk_save_objects(list_teamgamelog_sqlalchemy)  # Insertion en batch

                db.flush()  # Flush avant commit pour s'assurer que les objets sont envoyés à la base de données
                db.commit()

                print(f"{count_teamgamelogs} nouveaux teamgamelogs ont été ajoutés à la base de données.")

            except Exception as e:
                db.rollback()
                print(f"Une erreur est survenue lors de l'ajout des teamgamelogs : {e}")

    @staticmethod
    def clear_teamgamelog_table():
        with SessionLocal() as session:
            try:
                # Vider la table en supprimant tous les enregistrements
                session.query(TeamGameLog).delete()
                session.commit()  # Valider les changements
                print("La table teamgamelog a été vidée avec succès.")
            except Exception as e:
                session.rollback()  # Annuler en cas d'erreur
                print(f"Une erreur est survenue lors du vidage de la table teamgamelog : {e}")

    @staticmethod
    def drop_teamgamelog_table():
        with SessionLocal() as session:
            try:
                # Supprimer la table TeamGameLog
                TeamGameLog.__table__.drop(bind=session.get_bind())
                print("La table teamgamelog a été supprimée avec succès.")
            except Exception as e:
                print(f"Une erreur est survenue lors de la suppression de la table teamgamelog : {e}")


if __name__ == "__main__":
    # TeamGameLogTableMgmt.fill_teamgamelog_table()
    TeamGameLogTableMgmt.update_teamgamelog_table()

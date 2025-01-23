from tqdm import tqdm

from app.database.db_connector import engine, SessionLocal
from app.models.teamgamelog import TeamGameLog
from app.services.team_service import TeamService
from app.services.teamgamelog_service import TeamGameLogService


class TeamGameLogTableLifeCycle:

    @staticmethod
    def create_teamgamelog_table():
        TeamGameLog.__table__.create(engine)

        print("Table 'teamgamelog' créée avec succès.")

    @staticmethod
    def fill_teamgamelog_table():

        # Récupérer la liste des ids de toutes les équipes dans la table team
        team_ids_list = TeamService.get_all_team_ids()

        # Boucle id d'équipe par id d'équipe
        with SessionLocal() as db:
            try:
                # La barre de progression avec tqdm
                for index, team_id in tqdm(enumerate(team_ids_list), desc="Ajout des teamgamelog", unit="teamgamelog", total=len(team_ids_list)):

                    # (Récupérer la liste des game_id de la table teamgamelog) : uniquement pour une méthode update, à lancer quotidiennement
                    # teamgamelog_in_base_list
                    # Appel API à TeamGameLog
                    teamgamelog_df = TeamGameLogService.get_teamgamelog_df_by_team_id(team_id)
                    # Passer tous les champs en minuscule
                    teamgamelog_df.columns = teamgamelog_df.columns.str.lower()
                    # (Conservation uniquement des lignes du dataframe de l'appel, avec un id qui n'est pas en base) : uniquement pour une méthode update, à lancer quotidiennement
                    # teamgamelog_df = teamgamelog_df[~teamgamelog_df['game_id'].isin(teamgamelog_in_base_list)]

                    # Boucle sur les lignes du DataFrame
                    for i, row in teamgamelog_df.iterrows():
                        teamgamelog_model = TeamGameLogService.map_row_teamgamelog_df_to_teamgamelog_model(row)
                        # print(type(teamgamelog_model))
                        db.add(teamgamelog_model)

                db.commit()
                print(f"Tous les {len(team_ids_list)} teamgamelogs disponibles ont été ajoutés à la base de données avec succès.")

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
    TeamGameLogTableLifeCycle.fill_teamgamelog_table()
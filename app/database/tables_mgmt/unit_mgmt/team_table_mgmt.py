from tqdm import tqdm

from app.database.db_connector import engine, SessionLocal
from app.models.team import Team
from app.services.nba_api_service import NbaApiService
from app.services.team_service import TeamService
from app.dto.team_dto import TeamDTO
from app.dao.team_dao import TeamDAO


class TeamTableMgmt:

    @staticmethod
    def create_team_table():
        Team.__table__.create(engine)

        print("Table 'team' créée avec succès.")

    @staticmethod
    def fill_team_table():

        # Récupération des équipes depuis l'API
        teams_list = NbaApiService.get_raw_teams()

        # Création de la liste de DTO
        team_dto_list = [
            TeamService.map_static_team_to_team_dto(team) for team in teams_list
        ]

        # Ajout de l'équipe "No team" à la liste
        team_dto_list.append(
            TeamDTO(team_id=0, team_full_name="No team", team_tricode="NT", team_city="No team")
        )

        # Boucler sur ces équipes
        with SessionLocal() as db:
            try:
                # La barre de progression avec tqdm
                for index, team in tqdm( # ne pas oublier l'index, qui évite de créer des tuples
                        enumerate(team_dto_list),
                        desc="Ajout des équipes",
                        unit="équipe",
                        total=len(team_dto_list)
                ):

                    team_sqlalchemy = TeamDAO.team_from_dto_to_sql(team)

                    # Ajouter l'entrée à la session sans valider
                    db.add(team_sqlalchemy)

                db.commit()
                print(f"Toutes les {len(teams_list)} équipes ont été ajoutées à la base de données avec succès.")

            except Exception as e:
                db.rollback()
                print(f"Une erreur est survenue lors de l'ajout des équipes : {e}")

    @staticmethod
    def clear_team_table():
        with SessionLocal() as session:
            try:
                # Vider la table en supprimant tous les enregistrements
                session.query(Team).delete()
                session.commit()  # Valider les changements
                print("La table team a été vidée avec succès.")
            except Exception as e:
                session.rollback()  # Annuler en cas d'erreur
                print(f"Une erreur est survenue lors du vidage de la table team : {e}")

    @staticmethod
    def drop_team_table():
        with SessionLocal() as session:
            try:
                # Supprimer la table Player
                Team.__table__.drop(bind=session.get_bind())
                print("La table team a été supprimée avec succès.")
            except Exception as e:
                print(f"Une erreur est survenue lors de la suppression de la table team : {e}")


if __name__ == "__main__":
    TeamTableMgmt.fill_team_table()
    #TeamTableMgmt.create_team_table()
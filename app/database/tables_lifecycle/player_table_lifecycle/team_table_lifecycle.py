import time
from tqdm import tqdm

from app.config import Config
from app.dao.team_dao import TeamDAO
from app.database.db_connector import engine, SessionLocal
from app.models.team import Team
from app.services.team_service import TeamService


class TeamTableLifeCycle:

    @staticmethod
    def create_team_table():
        # Base.metadata.create_all(engine) # Pour créer toutes les classes héritant de Base
        Team.__table__.create(engine)

        print("Table 'team' créée avec succès.")

    @staticmethod
    def fill_team_table():
        # TODO : rajouter l'équipe en 0 No team
        teams_list = TeamService.get_teams()
        # Boucler sur ces joueurs en ajoutant leurs informations avec CommonPlayerInfo
        with SessionLocal() as db:
            try:
                # La barre de progression avec tqdm
                for team in tqdm(enumerate(teams_list), desc="Ajout des équipes", unit="équipe", total=len(teams_list)):
                    team_dto = TeamService.map_static_team_to_team_dto(team)

                    # Conversion du DTO en model Team
                    team_sql = TeamDAO.team_dto_to_sqlalchemy(team_dto)

                    # Ajouter l'entrée à la session sans valider
                    db.add(team_sql)

                db.commit()
                print(f"Toutes les {len(teams_list)} équipes ont été ajoutées à la base de données avec succès.")

            except Exception as e:
                db.rollback()
                print(f"Une erreur est survenue lors de l'ajout des joueurs : {e}")

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

if __name__ == "__main__":
    TeamTableLifeCycle.fill_team_table()
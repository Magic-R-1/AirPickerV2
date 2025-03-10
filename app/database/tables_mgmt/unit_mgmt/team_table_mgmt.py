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
        teams_df = NbaApiService.get_teams()

        # Création de la liste de DTO
        # On utilise les DTO pour bénéficier de son contrôle strict des données, et ainsi ajouter "No team"
        # Le faible nombre ne pousse pas à rester sur un DataFrame pour les performances
        team_dto_list = [
            TeamService.map_team_tuple_to_team_dto(row) for row in teams_df.itertuples(index=False)
        ]

        # Ajout de l'équipe "No team" à la liste
        team_dto_list.append(
            TeamDTO(team_id=0, team_full_name="No team", team_tricode="NT", team_city="No team")
        )

        # Boucler sur ces équipes
        with SessionLocal() as db:
            try:
                # La barre de progression avec tqdm
                for team in tqdm(
                        team_dto_list,
                        desc="Ajout des équipes",
                        unit="équipe",
                        total=len(team_dto_list)
                ):

                    team_sqlalchemy = TeamDAO.team_from_dto_to_sql(team)
                    db.add(team_sqlalchemy)

                db.commit()
                print(f"Toutes les {len(team_dto_list)} équipes ont été ajoutées à la base de données avec succès.")

            except Exception as e:
                db.rollback()
                print(f"Une erreur est survenue lors de l'ajout des équipes : {e}")

    @staticmethod
    # TODO
    def update_team_table():
        print("")

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
    #TeamTableMgmt.create_team_table()
    #TeamTableMgmt.drop_team_table()
    TeamTableMgmt.fill_team_table()

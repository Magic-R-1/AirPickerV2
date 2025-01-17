from app.database.db_connector import SessionLocal, engine
from app.dto.team_dto import TeamDTO
from app.exceptions.exceptions import TeamNotFoundError
from app.models.team import Team


class TeamDAO:

    # 1. CRUD
    # =================================

    @staticmethod
    def get_team_by_id(team_id: int):
        with SessionLocal() as session:
            team_from_sql = session.query(Team).filter_by(team_id=team_id).first()
            if team_from_sql is None:
                raise TeamNotFoundError(f"Équipe avec l'id '{team_id}' non trouvée.")
            return team_from_sql

    # 2. Utils
    # =================================

    @staticmethod
    def teams_from_sqlalchemy_to_dto(sqlalchemy_obj):
        """
        Convertit un objet ou une liste d'objets SQLAlchemy en une ou plusieurs instances de TeamDTO.
        :param sqlalchemy_obj: Un objet ou une liste d'objets SQLAlchemy.
        :return: Une instance ou une liste d'instances de TeamDTO.
        """
        def convert_to_dto(obj):
            """ Convertit un seul objet SQLAlchemy en TeamDTO """
            attributes = {key: value for key, value in vars(obj).items() if not key.startswith('_')}
            return TeamDTO(**attributes)

        # Si l'argument est une liste, on parcourt chaque élément et on les convertit
        if isinstance(sqlalchemy_obj, list):
            return [convert_to_dto(obj) for obj in sqlalchemy_obj]

        # Si c'est un seul objet, on le convertit directement en TeamDTO
        return convert_to_dto(sqlalchemy_obj)

    @staticmethod
    def team_dto_to_sqlalchemy(team_dto: TeamDTO):
        if isinstance(team_dto, list):
            # Si l'entrée est une liste, on la convertit en une liste d'objets Team
            return [Team(**{k: v for k, v in vars(p).items() if hasattr(Team, k)}) for p in team_dto]
        else:
            # Si l'entrée est un seul objet, on le convertit directement
            return Team(**{k: v for k, v in vars(team_dto).items() if hasattr(Team, k)})

if __name__ == "__main__":
    team_sql = TeamDAO.get_team_by_id(1610612763)
    team_dto = TeamDAO.teams_from_sqlalchemy_to_dto(team_sql)
    print("toto")

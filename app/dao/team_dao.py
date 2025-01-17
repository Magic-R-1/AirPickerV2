from app.database.db_connector import SessionLocal, engine
from app.dto.team_dto import TeamDTO
from app.models.team import Team


class TeamDAO:

    # 1. CRUD
    # =================================

    # 2. Utils
    # =================================

    @staticmethod
    def team_dto_to_sqlalchemy(team_dto: TeamDTO):
        if isinstance(team_dto, list):
            # Si l'entrée est une liste, on la convertit en une liste d'objets Team
            return [Team(**{k: v for k, v in vars(p).items() if hasattr(Team, k)}) for p in team_dto]
        else:
            # Si l'entrée est un seul objet, on le convertit directement
            return Team(**{k: v for k, v in vars(team_dto).items() if hasattr(Team, k)})
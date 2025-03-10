from typing import List, Tuple

from app.database.db_connector import session_scope
from app.dto.teamgamelog_dto import TeamGameLogDTO
from app.exceptions.exceptions import TeamGameLogNotFoundError
from app.models.teamgamelog import TeamGameLog
from app.schemas.teamgamelog_schema import TeamGameLogSchema


class TeamGameLogDAO:

    # 1. CRUD
    # =================================

    @staticmethod
    def add_teamgamelog(teamgamelog_dto: TeamGameLogDTO):
        try:
            # Convertir le TeamGameLogDTO en objet TeamGameLog
            teamgamelog_sqlalchemy = TeamGameLogDAO.teamgamelog_from_dto_to_sql(teamgamelog_dto)

            # Ajouter l'objet TeamGameLog à la session SQLAlchemy
            with session_scope() as session:
                session.add(teamgamelog_sqlalchemy)
                session.commit()
                session.refresh(teamgamelog_sqlalchemy)
                return teamgamelog_sqlalchemy  # Retourner l'objet TeamGameLog nouvellement ajouté

        except Exception as e:
            print(f"Erreur lors de l'ajout du joueur : {e}")
            return None

    @staticmethod
    def get_teamgamelog_by_pk(team_id: int, game_id: int):
        with session_scope() as session:
            teamgamelog_from_sql = session.query(TeamGameLog).get((team_id, game_id))
            if teamgamelog_from_sql is None:
                raise TeamGameLogNotFoundError(f"TeamGameLog avec l'id '{team_id}' et '{game_id}' non trouvé.")
            return teamgamelog_from_sql

    @staticmethod
    def get_teamgamelogs_by_team_id(team_id: int):
        with session_scope() as session:
            teamgamelogs_from_sql = session.query(TeamGameLog).filter_by(team_id=team_id).all()
            if teamgamelogs_from_sql is None:
                raise TeamGameLogNotFoundError(f"Liste de TeamGameLog avec l'id d'équipe '{team_id}' non trouvée.")
            return teamgamelogs_from_sql

    @staticmethod
    def get_list_pk_by_team_id(team_id: int) -> List[Tuple[int, str]]:
        with session_scope() as session:
            # Récupérer la liste des tuples (team_id, game_id) pour une équipe donnée
            list_pk = session.query(TeamGameLog.team_id, TeamGameLog.game_id) \
                .filter(TeamGameLog.team_id == team_id) \
                .all()

        return list_pk

    @staticmethod
    def get_list_game_id_by_team_id(team_id: int) -> List[str]:
        with session_scope() as session:
            # Récupérer la liste des game_id pour une équipe donnée
            list_game_ids = session.query(TeamGameLog.game_id) \
                .filter(TeamGameLog.team_id == team_id) \
                .all()

        # Extraire les IDs des matchs à partir des tuples
        return [game_id[0] for game_id in list_game_ids]

    @staticmethod
    def get_all_teamgamelogs():
        with session_scope() as session:
            teamgamelogs_from_sql = session.query(TeamGameLog).all()
            if teamgamelogs_from_sql is None:
                raise TeamGameLogNotFoundError(f"Aucun TeamGameLog trouvé.")
            return teamgamelogs_from_sql

    @staticmethod
    def get_list_unique_game_ids() -> List[str]:
        """
        Récupère la liste des game_id uniques depuis la table teamgamelog.

        :return: Liste des game_id uniques.
        """
        with session_scope() as session:
            unique_game_ids = session.query(TeamGameLog.game_id).distinct().all()
            return [row[0] for row in unique_game_ids]

    # 2. Utils
    # =================================

    @staticmethod
    def teamgamelog_from_dto_to_sql(teamgamelog_dto: TeamGameLogDTO):
        """
        Convertit une instance TeamGameLogDTO en une instance SQLAlchemy TeamGameLog en passant par TeamGameLogSchema.

        :param teamgamelog_dto: Instance de TeamGameLogDTO contenant les données.
        :return: Instance SQLAlchemy du modèle TeamGameLog.
        """
        # Convertir TeamGameLogDTO en dictionnaire
        teamgamelog_schema = TeamGameLogSchema().dump(teamgamelog_dto)
        # Créer une instance SQLAlchemy TeamGameLog
        return TeamGameLog(**teamgamelog_schema)

    @staticmethod
    def teamgamelog_from_sql_to_dto(teamgamelog_sqlalchemy: TeamGameLogDTO):
        """
        Convertit une instance SQLAlchemy TeamGameLog en une instance TeamGameLogDTO.

        :param teamgamelog_sqlalchemy: Instance SQLAlchemy du modèle TeamGameLog.
        :return: Instance de TeamGameLogDTO.
        """
        # Sérialisation avec Marshmallow
        teamgamelog_schema = TeamGameLogSchema().dump(teamgamelog_sqlalchemy)
        # Création de l'instance TeamGameLogDTO
        return TeamGameLogDTO(**teamgamelog_schema)


if __name__ == "__main__":
    # myList = TeamGameLogDAO.get_list_pk_by_team_id(1610612737)
    myList = TeamGameLogDAO.get_list_game_id_by_team_id(1610612737)
    print("")

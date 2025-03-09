from builtins import list
from marshmallow import ValidationError
import pandas as pd
from pandas import DataFrame

from app.models.teamgamelog import TeamGameLog
from app.schemas.teamgamelog_schema import TeamGameLogSchema
from app.dao.teamgamelog_dao import TeamGameLogDAO
from app.dto.teamgamelog_dto import TeamGameLogDTO


class TeamGameLogService:

    def __init__(self):
        pass

    @staticmethod
    def get_list_teamgamelog_dto_by_team_id(team_id: int) -> list[TeamGameLogDTO]:
        """
        Récupère une liste de TeamGameLogDTO pour un team_id donné.

        :param team_id: L'ID de l'équipe dont les TeamGameLogs sont recherchés.
        :return: Liste d'instances de TeamGameLogDTO.
        :raises TeamGameLogNotFoundError: Si aucun TeamGameLog n'est trouvé pour l'équipe donnée.
        """
        # Récupérer les TeamGameLog depuis la base
        teamgamelogs_from_sql = TeamGameLogDAO.get_teamgamelogs_by_team_id(team_id)

        # Convertir chaque TeamGameLog en DTO
        teamgamelogs_dto = [
            TeamGameLogDAO.teamgamelog_from_sql_to_dto(teamgamelog)
            for teamgamelog in teamgamelogs_from_sql
        ]

        return teamgamelogs_dto

    @staticmethod
    def get_df_all_teamgamelogs() -> DataFrame:

        teamgamelogs_from_sql = TeamGameLogDAO.get_all_teamgamelogs()

        # Utilisation de la méthode `__dict__` pour obtenir les attributs des objets en dictionnaire
        teamgamelogs_dict = [teamgamelog.__dict__ for teamgamelog in teamgamelogs_from_sql]

        # Convertir la liste de dictionnaires en DataFrame
        df_teamgamelogs = pd.DataFrame(teamgamelogs_dict)

        # df_teamgamelogs = Utils.obtenir_df_manipulable(df_teamgamelogs)

        # Supprimer la colonne '__table__' ajoutée par SQLAlchemy pour l'auto-référence
        if '_sa_instance_state' in df_teamgamelogs.columns:
            df_teamgamelogs.drop('_sa_instance_state', axis=1, inplace=True)

        return df_teamgamelogs

    @staticmethod
    def get_df_pk_teamgamelog_by_team_id(team_id: int) -> DataFrame:

        list_pk = TeamGameLogDAO.get_list_pk_by_team_id(team_id)

        # Transformer le résultat de la requête en DataFrame
        df_pk = pd.DataFrame(list_pk, columns=["team_id", "game_id"])

        return df_pk

    @staticmethod
    def map_df_teamgamelog_to_list_teamgamelog_model(teamgamelog_df: DataFrame) -> list[TeamGameLog: dict]:
        """
        Cette méthode prend un DataFrame et le convertit en une liste de TeamGameLog.

        :param teamgamelog_df: DataFrame contenant les données des matchs
        :return: Liste de dictionnaires représentant les objets TeamGameLog
        """
        teamgamelog_dict = teamgamelog_df.to_dict(orient='records')  # Convertir le DataFrame en liste de dicts
        list_teamgamelog = []

        for teamgamelog_row in teamgamelog_dict:
            try:
                teamgamelog_schema = TeamGameLogSchema().load(teamgamelog_row)
                teamgamelog_model = TeamGameLog(**teamgamelog_schema)
                list_teamgamelog.append(teamgamelog_model)

            except ValidationError as err:
                print(f"Erreur de validation sur la ligne {teamgamelog_row}: {err.messages}")
                raise  # Planter le code si passage ici

        return list_teamgamelog


if __name__ == "__main__":
    # teamgamelog_df = TeamGameLogService.get_teamgamelog_df_from_api_by_team_id(1610612742)
    my_list = TeamGameLogService.get_list_teamgamelog_dto_by_team_id(1610612737)
    print("toto")

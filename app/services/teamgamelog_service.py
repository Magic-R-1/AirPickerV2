from builtins import list

from pandas import Series

from app.models.teamgamelog import TeamGameLog
from app.schemas.teamgamelog_schema import TeamGameLogSchema
from app.services.nba_api_service import NbaApiService
from app.utils.utils import Utils
from marshmallow import ValidationError
import pandas as pd

from dao.teamgamelog_dao import TeamGameLogDAO
from dto.teamgamelog_dto import TeamGameLogDTO


class TeamGameLogService:

    def __init__(self):
        pass

    @staticmethod
    def get_df_teamgamelog_from_api_by_team_id(team_id: int) -> pd.DataFrame:
        return NbaApiService.get_team_game_log_by_team_id(team_id)

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
    def get_df_all_teamgamelogs() -> pd.DataFrame:

        teamgamelogs_from_sql = TeamGameLogDAO.get_all_teamgamelogs()

        # Utilisation de la méthode `__dict__` pour obtenir les attributs des objets en dictionnaire
        teamgamelogs_dict = [teamgamelog.__dict__ for teamgamelog in teamgamelogs_from_sql]

        # Convertir la liste de dictionnaires en DataFrame
        df_teamgamelogs = pd.DataFrame(teamgamelogs_dict)

        # Supprimer la colonne '__table__' ajoutée par SQLAlchemy pour l'auto-référence
        if '_sa_instance_state' in df_teamgamelogs.columns:
            df_teamgamelogs.drop('_sa_instance_state', axis=1, inplace=True)

        return df_teamgamelogs

    @staticmethod
    def get_df_pk_teamgamelog_by_team_id(team_id: int) -> pd.DataFrame:

        list_pk = TeamGameLogDAO.get_list_pk_by_team_id(team_id)

        # Transformer le résultat de la requête en DataFrame
        df_pk = pd.DataFrame(list_pk, columns=["team_id", "game_id"])

        return df_pk

    @staticmethod
    def map_df_teamgamelog_to_teamgamelog_models(teamgamelog_df: pd.DataFrame) -> list[TeamGameLog: dict]:
        """
        Cette méthode prend un DataFrame et le convertit en une liste de TeamGameLog
        en utilisant le schema Marshmallow.

        :param teamgamelog_df: DataFrame contenant les données des matchs
        :return: Liste de dictionnaires représentant les objets TeamGameLog
        """
        team_game_logs = []

        for index, row in teamgamelog_df.iterrows():
            # Désérialiser la ligne en un objet TeamGameLog
            teamgamelog_model = TeamGameLogService.map_row_teamgamelog_df_to_teamgamelog_model(row)
            team_game_logs.append(teamgamelog_model)

        return team_game_logs

    @staticmethod
    def map_row_teamgamelog_df_to_teamgamelog_model(row: Series) -> TeamGameLog | None :
        """
        Cette méthode prend un dictionnaire représentant une ligne de données et le convertit
        en un objet TeamGameLog en utilisant le schema Marshmallow.

        :param row: Ligne du DF représentant les données d'un match
        :return: Un objet TeamGameLog
        """

        try:
            # Convertir la ligne en dictionnaire
            row_dict = dict(row)

            # Sérialiser les données avec Marshmallow
            team_game_log_data = TeamGameLogSchema().dump(row_dict)

            # Créer une instance SQLAlchemy TeamGameLog à partir du dictionnaire créé par Marshmallow
            return TeamGameLog(**team_game_log_data)

        except ValidationError as err:
            print(f"Erreur de validation: {err.messages}")
            return None

if __name__ == "__main__":

    #teamgamelog_df = TeamGameLogService.get_teamgamelog_df_from_api_by_team_id(1610612742)
    my_list = TeamGameLogService.get_list_teamgamelog_dto_by_team_id(1610612737)
    print("toto")
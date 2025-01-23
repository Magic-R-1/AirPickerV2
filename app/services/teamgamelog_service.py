from app.models import TeamGameLog
from app.schemas.teamgamelog_schema import TeamGameLogSchema
from app.services.nba_api_service import NbaApiService
from app.utils.utils import Utils
from marshmallow import ValidationError
import pandas as pd


class TeamGameLogService:

    def __init__(self):
        pass

    @staticmethod
    def get_teamgamelog_df_by_team_id(team_id: int):
        teamgamelog_data = NbaApiService.get_team_game_log_by_team_id(team_id)
        teamgamelog_df = Utils.obtenir_df_manipulable(teamgamelog_data)

        return teamgamelog_df

    @staticmethod
    def map_teamgamelog_df_to_teamgamelog_models(teamgamelog_df: pd.DataFrame):
        """
        Cette méthode prend un DataFrame et le convertit en une liste de TeamGameLog
        en utilisant le schema Marshmallow.

        :param teamgamelog_df: DataFrame contenant les données des matchs
        :return: Liste de dictionnaires représentant les objets TeamGameLog
        """
        team_game_log_schema = TeamGameLogSchema()
        team_game_logs = []

        for index, row in teamgamelog_df.iterrows():
            # Désérialiser la ligne en un objet TeamGameLog
            teamgamelog_model = TeamGameLogService.map_row_teamgamelog_df_to_teamgamelog_model(row)
            team_game_logs.append(teamgamelog_model)

        return team_game_logs

    @staticmethod
    def map_row_teamgamelog_df_to_teamgamelog_model(row):
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

    teamgamelog_df = TeamGameLogService.get_teamgamelog_df_by_team_id(1610612742)
    print("toto")
from typing import Optional

import pandas as pd

from app.dto.player_dto import PlayerDTO
from app.dao.player_dao import PlayerDAO
from app.exceptions.exceptions import PlayerNotFoundError
from app.schemas.player_schema import PlayerSchema
from app.services.nba_api_service import NbaApiService
from app.utils.utils import Utils
from app.enums.nba_api_endpoints import NbaApiEndpoints
from app.models.player import Player
from utils.nba_api_column_mapper import NbaApiColumnMapper


class PlayerService:

    def __init__(self):
        pass

    @staticmethod
    def get_player_dto_by_display_first_last(player_name: str):

        try:
            player_sql = PlayerDAO.get_player_by_display_first_last(player_name)
        except (PlayerNotFoundError, ValueError) as e:
            print(f"Erreur: {e}")
            return None

        player_dto = PlayerDAO.player_from_sql_to_dto(player_sql)

        return player_dto

    @staticmethod
    def map_common_player_info_to_player_model(player_data):
        """
        Convertit les données de l'API NBA en Player en utilisant PlayerSchema.

        :param player_data: Dictionnaire contenant les données de l'API NBA.
        :return: Instance de Player.
        """
        try:
            # Convertir la première ligne du DataFrame en dictionnaire
            player_dict = player_data.iloc[0].to_dict()

            # Utilisation de PlayerSchema pour valider et structurer les données
            player_schema = PlayerSchema().load(player_dict)  # Valide et prépare les données

            # Création de Player à partir des données validées
            return Player(**player_schema)

        except Exception as e:
            print(f"Erreur lors du mapping des données du joueur : {e}")
            return None

    @staticmethod
    def map_common_player_info_to_player_dto(player_data):
        """
        Convertit les données de l'API NBA en PlayerDTO en utilisant PlayerSchema.

        :param player_data: Dictionnaire contenant les données de l'API NBA.
        :return: Instance de PlayerDTO.
        """
        try:
            # Convertir la première ligne du DataFrame en dictionnaire
            player_dict = player_data.iloc[0].to_dict()

            # Utilisation de PlayerSchema pour valider et structurer les données
            player_schema = PlayerSchema().load(player_dict)  # Valide et prépare les données

            # Création de PlayerDTO à partir des données validées
            return PlayerDTO(**player_schema)

        except Exception as e:
            print(f"Erreur lors du mapping des données du joueur : {e}")
            return None

    @staticmethod
    def get_df_common_player_info_by_player_id(player_id: int) -> Optional[pd.DataFrame]:
        """
        Récupère les informations communes d'un joueur à partir de l'API NBA
        et retourne un DataFrame manipulable avec des colonnes renommées.

        :param player_id: L'identifiant unique du joueur.
        :return: Un DataFrame contenant les données du joueur ou None en cas d'erreur.
        """
        try:
            # Étape 1 : Récupération des données brutes depuis l'API
            player_data = NbaApiService.get_raw_common_player_info(player_id)

            # Étape 2 : Conversion des données en DataFrame manipulable
            df_player_data = Utils.obtenir_df_manipulable(player_data)

            # Étape 3 : Conversion des valeurs "YES/NO" en booléens
            df_player_data = Utils.convert_y_n_to_boolean(df_player_data)

            # Étape 4 : Renommage des colonnes selon le mapper défini
            df_player_data = NbaApiColumnMapper.rename_columns_in_df(
                df_player_data, NbaApiEndpoints.COMMON_PLAYER_INFO.value
            )

            return df_player_data

        except Exception as e:
            # Logging d'une erreur (si un logger est configuré)
            print(f"Erreur lors de la récupération des données pour le joueur {player_id}: {e}")
            return None

    @staticmethod
    def get_df_active_players():

        df_players = NbaApiService.get_players()
        df_filtered = df_players[df_players['is_active']]

        return df_filtered


if __name__ == "__main__":

    player_info = PlayerService.get_df_common_player_info_by_player_id(2544)
    player_dto = PlayerService.map_common_player_info_to_player_dto(player_info)
    print(player_dto)
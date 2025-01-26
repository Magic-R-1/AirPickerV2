import pandas as pd

from app.dto.player_dto import PlayerDTO
from app.dao.player_dao import PlayerDAO
from app.exceptions.exceptions import PlayerNotFoundError
from app.schemas.player_schema import PlayerSchema
from app.services.nba_api_service import NbaApiService
from app.models.player import Player


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
    def map_common_player_info_df_to_player_model(player_df):
        """
        Convertit les données de l'API NBA en Player en utilisant PlayerSchema.

        :param player_df: DataFrame contenant les données du joueur.
        :return: Instance de Player.
        """
        try:
            # Convertir la première ligne du DataFrame en dictionnaire
            player_dict = player_df.iloc[0].to_dict()

            # Utilisation de PlayerSchema pour valider et structurer les données
            player_schema = PlayerSchema().load(player_dict)

            # Création de Player à partir des données validées
            return Player(**player_schema)

        except Exception as e:
            print(f"Erreur lors du mapping des données du joueur : {e}")
            return None

    @staticmethod
    def map_common_player_info_df_to_player_dto(player_df):
        """
        Convertit les données de l'API NBA en PlayerDTO en utilisant PlayerSchema.

        :param player_df: Dictionnaire contenant les données de l'API NBA.
        :return: Instance de PlayerDTO.
        """
        try:
            # Convertir la première ligne du DataFrame en dictionnaire
            player_dict = player_df.iloc[0].to_dict()

            # Utilisation de PlayerSchema pour valider et structurer les données
            player_schema = PlayerSchema().load(player_dict)  # Valide et prépare les données

            # Création de PlayerDTO à partir des données validées
            return PlayerDTO(**player_schema)

        except Exception as e:
            print(f"Erreur lors du mapping des données du joueur : {e}")
            return None

    @staticmethod
    def get_df_common_player_info_by_player_id(player_id: int) -> pd.DataFrame | None:
        """
        Utile la méthode de NbaApiService pour obtenir le DF de common_player_info

        :param player_id: L'identifiant unique du joueur.
        :return: Un DataFrame contenant les données du joueur ou None en cas d'erreur.
        """
        try:
            return NbaApiService.get_common_player_info(player_id)

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
    player_dto = PlayerService.map_common_player_info_df_to_player_dto(player_info)
    print(player_dto)
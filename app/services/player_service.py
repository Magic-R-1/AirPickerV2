from app.dto.player_dto import PlayerDTO
from app.dao.player_dao import PlayerDAO
from app.exceptions.exceptions import PlayerNotFoundError
from app.schemas.player_schema import PlayerSchema
from app.services.nba_api_service import NbaApiService
from app.utils.utils import Utils


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
    def map_common_player_info_to_player_dto(player_data):
        """
        Convertit les données de l'API NBA en PlayerDTO en utilisant PlayerSchema.

        :param player_data: Dictionnaire contenant les données de l'API NBA.
        :return: Instance de PlayerDTO.
        """
        try:
            # Convertir la première ligne du DataFrame en dictionnaire
            player_dict = player_data.iloc[0].to_dict()
            # Renommer les clés avec un nom différent entre l'API NBA et PlayerSchema
            player_dict['PERSON_ID'] = player_dict.pop('PLAYER_ID')
            player_dict['PLAYER_CODE'] = player_dict.pop('PLAYERCODE')
            player_dict['ROSTER_STATUS'] = player_dict.pop('ROSTERSTATUS')
            # Mettre les clés en minuscules
            player_dict = {key.lower(): value for key, value in player_dict.items()}

            # Utilisation de PlayerSchema pour valider et structurer les données
            player_schema = PlayerSchema().load(player_dict)  # Valide et prépare les données

            # Création de PlayerDTO à partir des données validées
            return PlayerDTO(**player_schema)

        except Exception as e:
            print(f"Erreur lors du mapping des données de l'équipe : {e}")
            return None

    @staticmethod
    def get_common_player_info_df_by_player_id(player_id: int):
        player_info = NbaApiService.get_common_player_info(player_id)
        player_data = Utils.obtenir_df_manipulable(player_info)
        player_data = Utils.convert_yes_no_to_boolean(player_data)

        return player_data

    @staticmethod
    def get_active_players():

        list_players = NbaApiService.get_players()

        # Compréhension de liste pour filtrer les joueurs actifs
        list_active_players = [player for player in list_players if player['is_active']]

        return list_active_players


if __name__ == "__main__":

    player_info = PlayerService.get_common_player_info_df_by_player_id(2544)
    player_dto = PlayerService.map_common_player_info_to_player_dto(player_info)
    print(player_dto)
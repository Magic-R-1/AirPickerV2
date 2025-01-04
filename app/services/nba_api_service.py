from nba_api.stats.static import players
from nba_api.stats.endpoints import commonplayerinfo

from app.utils.utils import Utils

class NbaApiService:
    def __init__(self):
        pass

    @staticmethod
    def get_players():
        return players.get_players()

    @staticmethod
    def common_player_info(person_id):
        return commonplayerinfo.CommonPlayerInfo(player_id=person_id)

    @staticmethod
    def common_player_info_to_df(person_id):
        player_info = NbaApiService.common_player_info(person_id)   # Méthode statique, donc doit être appelée avec le nom de la classe
        player_data = player_info.get_data_frames()[0]              # Obtient le DataFrame des informations du joueur
        player_data = Utils.convert_yes_no_to_boolean(player_data)
        player_data = player_data.astype(object)                    # Convertir les types NumPy en types natifs Python, évite psycopg2: can't adapt type 'numpy.int64'

        return player_data

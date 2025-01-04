from nba_api.stats.static import players
from nba_api.stats.endpoints import commonplayerinfo

class NbaApiService:
    def __init__(self):
        pass

    @staticmethod
    def get_players():
        return players.get_players()

    @staticmethod
    def common_player_info(person_id):
        return commonplayerinfo.CommonPlayerInfo(player_id=person_id)

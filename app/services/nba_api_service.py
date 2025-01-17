from nba_api.stats.static import players, teams
from nba_api.stats.endpoints import commonplayerinfo

class NbaApiService:
    def __init__(self):
        pass

    # 1. Players
    # =================================

    @staticmethod
    def get_players():
        return players.get_players()

    @staticmethod
    def common_player_info(person_id):
        return commonplayerinfo.CommonPlayerInfo(player_id=person_id)

    # 2. Teams
    # =================================

    @staticmethod
    def get_teams():
        return teams.get_teams()

if __name__ == "__main__":
    list_teams = NbaApiService.get_teams()
    print("toto")
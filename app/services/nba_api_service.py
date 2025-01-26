from nba_api.stats.static import players, teams
from nba_api.stats.endpoints import boxscoretraditionalv3, commonplayerinfo, commonteamroster, playergamelog, playernextngames, teamgamelog
# scoreboardv2 : permet d’obtenir les matchs programmés pour une date précise

from config.config import Config


class NbaApiService:
    def __init__(self):
        pass

#TODO : renommer ici les données. Ne pas en changer la nature (list, df, etc.), mais les renommer d'entrée

    # 1. Player
    # =================================
    @staticmethod #TODO
    def get_players():
        return players.get_players()

    @staticmethod #Done
    def get_common_player_info(player_id):
        return commonplayerinfo.CommonPlayerInfo(player_id=player_id)

    @staticmethod #TODO
    def get_player_game_log_by_player_id(player_id: int):
        return playergamelog.PlayerGameLog(player_id=player_id, season=Config.SAISON_EN_COURS)

    @staticmethod #TODO
    def get_player_next_games_by_player_id(player_id: int):
        return playernextngames.PlayerNextNGames(player_id=player_id)

    # 2. Team
    # =================================
    @staticmethod #Done
    def get_teams():
        return teams.get_teams()

    @staticmethod #TODO
    def get_team_game_log_by_team_id(team_id: int):
        return teamgamelog.TeamGameLog(team_id=team_id, season=Config.SAISON_EN_COURS)

    @staticmethod #TODO
    def get_team_roster_by_team_id(team_id: int):
        return commonteamroster.CommonTeamRoster(team_id=team_id)

    # 3. Feuilles de match
    # =================================
    @staticmethod #TODO
    def get_boxscore_by_game_id(game_id: str):  #str car les id des matchs commencent par 00, effacés avec un int
        return boxscoretraditionalv3.BoxScoreTraditionalV3(game_id=game_id)


if __name__ == "__main__":
    # data = NbaApiService.get_boxscore_by_game_id("0022400596")
    print("")
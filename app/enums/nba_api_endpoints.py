from enum import Enum

class NbaApiEndpoints(Enum):

    # Endpoint
    COMMON_PLAYER_INFO = "commonplayerinfo"
    PLAYER_GAME_LOG = "playergamelog"
    PLAYER_NEXT_N_GAMES = "playernextngames"

    TEAM_GAME_LOG = "teamgamelog"
    COMMON_TEAM_ROSTER = "commonteamroster"

    BOX_SCORE_TRADITIONAL_V3 = "boxscoretraditionalv3"
    SCORE_BOARD_V2 = "scoreboardv2"

    # Static
    TEAMS_GET_TEAMS = "teams.get_teams"
    PLAYERS_GET_PLAYERS = "players.get_players"

if __name__ == "__main__":
    # Exemple d'utilisation
    print(NbaApiEndpoints.BOX_SCORE_TRADITIONAL_V3.value)
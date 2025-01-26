import pandas as pd
from nba_api.stats.static import players, teams
from nba_api.stats.endpoints import boxscoretraditionalv3, commonplayerinfo, commonteamroster, playergamelog, playernextngames, teamgamelog
# scoreboardv2 : permet d’obtenir les matchs programmés pour une date précise

from app.config.config import Config
from app.utils.nba_api_column_mapper import NbaApiColumnMapper
from app.enums.nba_api_endpoints import NbaApiEndpoints
from app.utils.utils import Utils


class NbaApiService:
    def __init__(self):
        pass

    # 1. Player
    # =================================
    @staticmethod # Done
    def get_raw_players():
        return players.get_players()

    @staticmethod # Liste de dictionnaires vers DataFrame # Done
    def get_players() -> pd.DataFrame:
        """
        Récupère les joueurs via l'API, les transforme en DataFrame et renomme les colonnes.
        :return: pd.DataFrame: Liste des joueurs.
        """

        list_dicts = NbaApiService.get_raw_players()
        df = pd.DataFrame(list_dicts)
        df_ameliore = Utils.ameliore_df(df)
        df_renamed = NbaApiColumnMapper.rename_columns_in_df(df_ameliore, NbaApiEndpoints.PLAYERS_GET_PLAYERS.value)
        return df_renamed

    @staticmethod #Done
    def get_raw_common_player_info(player_id):
        return commonplayerinfo.CommonPlayerInfo(player_id=player_id)

    @staticmethod # Objet brut CommonPlayerInfo vers DataFrame # Done
    def get_common_player_info(player_id):
        """
        Récupère l'objet CommonPlayerInfo via l'API, le transforme en DataFrame et renomme les colonnes.
        :return: pd.DataFrame: Informations des joueurs.
        """

        raw_data = NbaApiService.get_raw_common_player_info(player_id)
        df = Utils.obtenir_df_manipulable(raw_data)
        df_renamed = NbaApiColumnMapper.rename_columns_in_df(df, NbaApiEndpoints.COMMON_PLAYER_INFO.value)
        return df_renamed

    @staticmethod #TODO
    def get_raw_player_game_log_by_player_id(player_id: int):
        return playergamelog.PlayerGameLog(player_id=player_id, season=Config.SAISON_EN_COURS)

    @staticmethod #TODO
    def get_raw_player_next_games_by_player_id(player_id: int):
        return playernextngames.PlayerNextNGames(player_id=player_id)

    # 2. Team
    # =================================
    @staticmethod #Done
    def get_raw_teams():
        return teams.get_teams()

    @staticmethod # Liste de dictionnaires vers DataFrame #Done
    def get_teams():
        """
        Récupère les équipes via l'API, les transforme en DataFrame et renomme les colonnes.
        :return: pd.DataFrame: Liste des équipes.
        """

        list_dicts = NbaApiService.get_raw_teams()
        df = pd.DataFrame(list_dicts)
        df_ameliore = Utils.ameliore_df(df)
        df_renamed = NbaApiColumnMapper.rename_columns_in_df(df_ameliore, NbaApiEndpoints.TEAMS_GET_TEAMS.value)
        return df_renamed

    @staticmethod #TODO
    def get_raw_team_game_log_by_team_id(team_id: int):
        return teamgamelog.TeamGameLog(team_id=team_id, season=Config.SAISON_EN_COURS)

    @staticmethod #TODO
    def get_raw_team_roster_by_team_id(team_id: int):
        return commonteamroster.CommonTeamRoster(team_id=team_id)

    # 3. Feuilles de match
    # =================================
    @staticmethod #TODO
    def get_raw_boxscore_by_game_id(game_id: str):  #str car les id des matchs commencent par 00, effacés avec un int
        return boxscoretraditionalv3.BoxScoreTraditionalV3(game_id=game_id)


if __name__ == "__main__":

    #data = NbaApiService.get_common_player_info(2544)
    data = NbaApiService.get_teams()
    
    print("")
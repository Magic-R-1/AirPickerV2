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
    @staticmethod
    def get_players() -> pd.DataFrame:
        """
        input : list[dict]
        Transformation en DataFrame, et renommage des colonnes.
        :return: pd.DataFrame: Liste des joueurs.
        """
        list_dicts = players.get_players()  # Appel API
        df = pd.DataFrame(list_dicts)
        df_ameliore = Utils.ameliore_df(df)
        df_renamed = NbaApiColumnMapper.rename_columns_in_df(df_ameliore, NbaApiEndpoints.PLAYERS_GET_PLAYERS.value)
        return df_renamed

    @staticmethod
    def get_common_player_info(player_id) -> pd.DataFrame:
        """
        input : objet commonplayerinfo
        Transformation en DataFrame, et renommage des colonnes.
        :return: pd.DataFrame: Informations du joueur.
        """
        raw_data = commonplayerinfo.CommonPlayerInfo(player_id=player_id)   # Appel API
        df = Utils.obtenir_df_manipulable(raw_data)
        df_renamed = NbaApiColumnMapper.rename_columns_in_df(df, NbaApiEndpoints.COMMON_PLAYER_INFO.value)
        return df_renamed

    @staticmethod
    def get_player_game_log_by_player_id(player_id: int) -> pd.DataFrame:
        """
        input : objet playergamelog
        Transformation en DataFrame, renommage des colonnes, et convertion des dates.
        :return: pd.DataFrame: Logs des boxscores du joueur.
        """
        raw_data = playergamelog.PlayerGameLog(player_id=player_id, season=Config.SAISON_EN_COURS)  # Appel API
        df = Utils.obtenir_df_manipulable(raw_data)
        df_renamed = NbaApiColumnMapper.rename_columns_in_df(df, NbaApiEndpoints.PLAYER_GAME_LOG.value)
        df_renamed["game_date"] = df_renamed["game_date"].apply(Utils.convert_to_date)  # Convertir les valeurs JUN 19, 2003 en Date 2003-06-19
        return df_renamed

    @staticmethod
    def get_player_next_games_by_player_id(player_id: int) -> pd.DataFrame:
        """
        input : objet playernextngames
        Transformation en DataFrame, renommage des colonnes, et convertion des dates.
        :return: pd.DataFrame: Logs des prochains matchs du joueur.
        """
        raw_data = playernextngames.PlayerNextNGames(player_id=player_id)   # Appel API
        df = Utils.obtenir_df_manipulable(raw_data)
        df_renamed = NbaApiColumnMapper.rename_columns_in_df(df, NbaApiEndpoints.PLAYER_GAME_LOG.value)
        df_renamed["game_date"] = df_renamed["game_date"].apply(Utils.convert_to_date)  # Convertir les valeurs JUN 19, 2003 en Date 2003-06-19
        return df_renamed

    # 2. Team
    # =================================
    @staticmethod
    def get_teams() -> pd.DataFrame:
        """
        input : list[dict]
        Transformation en DataFrame, et renommage des colonnes.
        :return: pd.DataFrame: Liste des équipes.
        """
        list_dicts = teams.get_teams()  # Appel API
        df = pd.DataFrame(list_dicts)
        df_ameliore = Utils.ameliore_df(df)
        df_renamed = NbaApiColumnMapper.rename_columns_in_df(df_ameliore, NbaApiEndpoints.TEAMS_GET_TEAMS.value)
        return df_renamed

    @staticmethod
    def get_team_roster_by_team_id(team_id: int) -> commonteamroster:
        """
        input : objet commonteamroster
        Transformation en DataFrame, renommage des colonnes, et convertion des dates.
        :return: pd.DataFrame: Informations des rosters.
        """
        raw_data = commonteamroster.CommonTeamRoster(team_id=team_id)   # Appel API
        df = Utils.obtenir_df_manipulable(raw_data)
        df_renamed = NbaApiColumnMapper.rename_columns_in_df(df, NbaApiEndpoints.COMMON_TEAM_ROSTER.value)
        df_renamed["birthdate"] = df_renamed["birthdate"].apply(Utils.convert_to_date)  # Convertir les valeurs JUN 19, 2003 en Date 2003-06-19
        return df_renamed

    @staticmethod
    def get_team_game_log_by_team_id(team_id: int) -> pd.DataFrame:
        """
        input : objet teamgamelog
        Transformation en DataFrame, renommage des colonnes, et convertion des dates.
        :return: pd.DataFrame: Logs des boxscores des équipes.
        """
        raw_data = teamgamelog.TeamGameLog(team_id=team_id, season=Config.SAISON_EN_COURS)  # Appel API
        df = Utils.obtenir_df_manipulable(raw_data)
        df_renamed = NbaApiColumnMapper.rename_columns_in_df(df, NbaApiEndpoints.TEAM_GAME_LOG.value)
        df_renamed["game_date"] = df_renamed["game_date"].apply(Utils.convert_to_date)  # Convertir les valeurs JUN 19, 2003 en Date 2003-06-19
        return df_renamed

    # 3. Feuilles de match
    # =================================
    @staticmethod
    def get_boxscore_by_game_id(game_id: str) -> pd.DataFrame:
        """
        input : objet boxscoretraditionalv3
        Transformation en DataFrame, et renommage des colonnes.
        :return: pd.DataFrame: Informations des boxscores.
        """
        raw_data = boxscoretraditionalv3.BoxScoreTraditionalV3(game_id=game_id) # Appel API
        df = Utils.obtenir_df_manipulable(raw_data)
        df_renamed = NbaApiColumnMapper.rename_columns_in_df(df, NbaApiEndpoints.BOX_SCORE_TRADITIONAL_V3.value)
        return df_renamed

if __name__ == "__main__":
    # data = NbaApiService.get_common_player_info(2544)
    # data = NbaApiService.get_teams()
    # data = NbaApiService.get_boxscore_by_game_id("0022400629")
    # data = NbaApiService.get_team_roster_by_team_id(1610612747)
    # data = NbaApiService.get_team_game_log_by_team_id(1610612747)
    # data = NbaApiService.get_player_game_log_by_player_id(2544)
    # data = NbaApiService.get_player_next_games_by_player_id(2544)
    
    print("")
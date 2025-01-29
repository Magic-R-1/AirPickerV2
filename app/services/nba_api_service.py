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
    def get_raw_players() -> list[dict]:
        return players.get_players()

    @staticmethod
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
    def get_raw_common_player_info(player_id) -> commonplayerinfo:
        return commonplayerinfo.CommonPlayerInfo(player_id=player_id)

    @staticmethod
    def get_common_player_info(player_id) -> pd.DataFrame:
        """
        Récupère l'objet CommonPlayerInfo via l'API, le transforme en DataFrame et renomme les colonnes.
        :return: pd.DataFrame: Informations des joueurs.
        """

        raw_data = NbaApiService.get_raw_common_player_info(player_id)
        df = Utils.obtenir_df_manipulable(raw_data)
        df_renamed = NbaApiColumnMapper.rename_columns_in_df(df, NbaApiEndpoints.COMMON_PLAYER_INFO.value)
        return df_renamed

    @staticmethod
    def get_raw_player_game_log_by_player_id(player_id: int) -> playergamelog:
        return playergamelog.PlayerGameLog(player_id=player_id, season=Config.SAISON_EN_COURS)

    @staticmethod
    def get_player_game_log_by_player_id(player_id: int) -> pd.DataFrame:
        """
        Récupère l'objet PlayerGameLog via l'API, le transforme en DataFrame, renomme les colonnes, et converti les dates.
        :return: pd.DataFrame: Logs des boxscores du joueur.
        """

        raw_data = NbaApiService.get_raw_player_game_log_by_player_id(player_id)
        df = Utils.obtenir_df_manipulable(raw_data)
        df_renamed = NbaApiColumnMapper.rename_columns_in_df(df, NbaApiEndpoints.PLAYER_GAME_LOG.value)
        df_renamed["game_date"] = df_renamed["game_date"].apply(Utils.convert_to_date)  # Convertir les valeurs JUN 19, 2003 en Date 2003-06-19
        return df_renamed

    #TODO
    @staticmethod
    def get_raw_player_next_games_by_player_id(player_id: int) -> playernextngames:
        return playernextngames.PlayerNextNGames(player_id=player_id)

    # 2. Team
    # =================================
    @staticmethod
    def get_raw_teams() -> list[dict]:
        return teams.get_teams()

    @staticmethod
    def get_teams() -> pd.DataFrame:
        """
        Récupère les équipes via l'API, les transforme en DataFrame et renomme les colonnes.
        :return: pd.DataFrame: Liste des équipes.
        """

        list_dicts = NbaApiService.get_raw_teams()
        df = pd.DataFrame(list_dicts)
        df_ameliore = Utils.ameliore_df(df)
        df_renamed = NbaApiColumnMapper.rename_columns_in_df(df_ameliore, NbaApiEndpoints.TEAMS_GET_TEAMS.value)
        return df_renamed

    @staticmethod
    def get_raw_team_roster_by_team_id(team_id: int) -> commonteamroster:
        return commonteamroster.CommonTeamRoster(team_id=team_id)

    @staticmethod
    def get_team_roster_by_team_id(team_id: int) -> commonteamroster:
        """
        Récupère l'objet CommonTeamRoster via l'API, le transforme en DataFrame, renomme les colonnes, et converti les dates.
        :return: pd.DataFrame: Informations des rosters.
        """

        raw_data = NbaApiService.get_raw_team_roster_by_team_id(team_id)
        df = Utils.obtenir_df_manipulable(raw_data)
        df_renamed = NbaApiColumnMapper.rename_columns_in_df(df, NbaApiEndpoints.COMMON_TEAM_ROSTER.value)
        df_renamed["birthdate"] = df_renamed["birthdate"].apply(Utils.convert_to_date)  # Convertir les valeurs JUN 19, 2003 en Date 2003-06-19
        return df_renamed

    @staticmethod
    def get_raw_team_game_log_by_team_id(team_id: int) -> teamgamelog:
        return teamgamelog.TeamGameLog(team_id=team_id, season=Config.SAISON_EN_COURS)

    @staticmethod
    def get_team_game_log_by_team_id(team_id: int) -> pd.DataFrame:
        """
        Récupère l'objet TeamGameLog via l'API, le transforme en DataFrame, renomme les colonnes, et converti les dates.
        :return: pd.DataFrame: Logs des boxscores des équipes.
        """

        raw_data = NbaApiService.get_raw_team_game_log_by_team_id(team_id)
        df = Utils.obtenir_df_manipulable(raw_data)
        df_renamed = NbaApiColumnMapper.rename_columns_in_df(df, NbaApiEndpoints.TEAM_GAME_LOG.value)
        df_renamed["game_date"] = df_renamed["game_date"].apply(Utils.convert_to_date)  # Convertir les valeurs JUN 19, 2003 en Date 2003-06-19
        return df_renamed

    # 3. Feuilles de match
    # =================================
    @staticmethod
    def get_raw_boxscore_by_game_id(game_id: str) -> boxscoretraditionalv3:
        return boxscoretraditionalv3.BoxScoreTraditionalV3(game_id=game_id)

    @staticmethod
    def get_boxscore_by_game_id(game_id: str) -> pd.DataFrame:
        """
        Récupère l'objet BoxScoreTraditionalV3 via l'API, le transforme en DataFrame et renomme les colonnes.
        :return: pd.DataFrame: Informations des boxscores.
        """

        raw_data = NbaApiService.get_raw_boxscore_by_game_id(game_id)
        df = Utils.obtenir_df_manipulable(raw_data)
        df_renamed = NbaApiColumnMapper.rename_columns_in_df(df, NbaApiEndpoints.BOX_SCORE_TRADITIONAL_V3.value)
        return df_renamed

if __name__ == "__main__":
    # data = NbaApiService.get_common_player_info(2544)
    # data = NbaApiService.get_teams()
    # data = NbaApiService.get_boxscore_by_game_id("0022400629")
    # data = NbaApiService.get_team_roster_by_team_id(1610612747)
    # data = NbaApiService.get_team_game_log_by_team_id(1610612747)
    data = NbaApiService.get_player_game_log_by_player_id(2544)
    
    print("")
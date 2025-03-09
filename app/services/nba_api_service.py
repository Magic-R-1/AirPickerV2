import pandas as pd
from nba_api.stats.static import players, teams
from nba_api.stats.endpoints import boxscoretraditionalv3, commonplayerinfo, commonteamroster, playergamelog, \
    playernextngames, teamgamelog, scoreboardv2

from datetime import date

from pandas import DataFrame

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
    def get_players() -> DataFrame:
        """
        input : list[dict]
        Transformation en DataFrame, et renommage des colonnes.
        :return: DataFrame : Liste des joueurs.
        """
        try:
            list_dicts = players.get_players()  # Appel API
        except Exception as e:
            print(f"Erreur lors de l'appel à get_players : {e}")
            list_dicts = []  # Valeur par défaut en cas d'échec

        df = pd.DataFrame(list_dicts)
        df_ameliore = Utils.ameliore_df(df)
        df_renamed = NbaApiColumnMapper.rename_columns_in_df(df_ameliore, NbaApiEndpoints.PLAYERS_GET_PLAYERS.value)
        return df_renamed

    @staticmethod
    def get_common_player_info(player_id) -> DataFrame:
        """
        input : objet commonplayerinfo
        Transformation en DataFrame, et renommage des colonnes.
        :return: DataFrame : Informations du joueur.
        """
        try:
            raw_data = commonplayerinfo.CommonPlayerInfo(player_id=player_id)  # Appel API
        except Exception as e:
            print(f"Erreur lors de l'appel à CommonPlayerInfo pour player_id={player_id} : {e}")
            raw_data = None  # Valeur par défaut en cas d'échec

        df = Utils.obtenir_df_manipulable(raw_data)
        df_renamed = NbaApiColumnMapper.rename_columns_in_df(df, NbaApiEndpoints.COMMON_PLAYER_INFO.value)
        return df_renamed

    @staticmethod
    def get_player_game_log_by_player_id(player_id: int) -> DataFrame:
        """
        input : objet playergamelog
        Transformation en DataFrame, renommage des colonnes, et convertion des dates.
        :return: DataFrame : Logs des boxscores du joueur.
        """
        try:
            raw_data = playergamelog.PlayerGameLog(player_id=player_id, season=Config.SAISON_EN_COURS)  # Appel API
        except Exception as e:
            print(
                f"Erreur lors de l'appel à PlayerGameLog pour player_id={player_id}, saison={Config.SAISON_EN_COURS} : {e}")
            raw_data = None  # Valeur par défaut en cas d'échec

        df = Utils.obtenir_df_manipulable(raw_data)
        df_renamed = NbaApiColumnMapper.rename_columns_in_df(df, NbaApiEndpoints.PLAYER_GAME_LOG.value)
        df_renamed["game_date"] = df_renamed["game_date"].apply(Utils.convert_to_date)
        return df_renamed

    @staticmethod
    def get_player_next_games_by_player_id(player_id: int) -> DataFrame:
        """
        input : objet playernextngames
        Transformation en DataFrame, renommage des colonnes, et convertion des dates.
        :return: DataFrame : Logs des prochains matchs du joueur.
        """
        try:
            raw_data = playernextngames.PlayerNextNGames(player_id=player_id)  # Appel API
        except Exception as e:
            print(f"Erreur lors de l'appel à PlayerNextNGames pour player_id={player_id} : {e}")
            raw_data = None  # Valeur par défaut en cas d'échec

        df = Utils.obtenir_df_manipulable(raw_data)
        df_renamed = NbaApiColumnMapper.rename_columns_in_df(df, NbaApiEndpoints.PLAYER_GAME_LOG.value)
        df_renamed["game_date"] = df_renamed["game_date"].apply(Utils.convert_to_date)
        return df_renamed

    # 2. Team
    # =================================
    @staticmethod
    def get_teams() -> DataFrame:
        """
        input : list[dict]
        Transformation en DataFrame, et renommage des colonnes.
        :return: DataFrame : Liste des équipes.
        """
        try:
            list_dicts = teams.get_teams()  # Appel API
        except Exception as e:
            print(f"Erreur lors de l'appel à get_teams : {e}")
            list_dicts = []  # Valeur par défaut en cas d'échec

        df = pd.DataFrame(list_dicts)
        df_ameliore = Utils.ameliore_df(df)
        df_renamed = NbaApiColumnMapper.rename_columns_in_df(df_ameliore, NbaApiEndpoints.TEAMS_GET_TEAMS.value)
        return df_renamed

    @staticmethod
    def get_team_roster_by_team_id(team_id: int) -> DataFrame:
        """
        input : objet commonteamroster
        Transformation en DataFrame, renommage des colonnes, et convertion des dates.
        :return: DataFrame : Informations des rosters.
        """
        try:
            raw_data = commonteamroster.CommonTeamRoster(team_id=team_id)  # Appel API
        except Exception as e:
            print(f"Erreur lors de l'appel à CommonTeamRoster avec team_id={team_id} : {e}")
            raw_data = None  # Valeur par défaut en cas d'échec

        df = Utils.obtenir_df_manipulable(raw_data)
        df_renamed = NbaApiColumnMapper.rename_columns_in_df(df, NbaApiEndpoints.COMMON_TEAM_ROSTER.value)
        df_renamed["birthdate"] = df_renamed["birthdate"].apply(Utils.convert_to_date)
        return df_renamed

    @staticmethod
    def get_team_game_log_by_team_id(team_id: int) -> DataFrame:
        """
        input : objet teamgamelog
        Transformation en DataFrame, renommage des colonnes, et convertion des dates.
        :return: DataFrame : Logs des boxscores des équipes.
        """
        try:
            raw_data = teamgamelog.TeamGameLog(team_id=team_id, season=Config.SAISON_EN_COURS)  # Appel API
        except Exception as e:
            print(f"Erreur lors de l'appel à TeamGameLog avec team_id={team_id}, season={Config.SAISON_EN_COURS} : {e}")
            raw_data = None  # Valeur par défaut en cas d'échec

        df = Utils.obtenir_df_manipulable(raw_data)
        df_renamed = NbaApiColumnMapper.rename_columns_in_df(df, NbaApiEndpoints.TEAM_GAME_LOG.value)
        df_renamed["game_date"] = df_renamed["game_date"].apply(Utils.convert_to_date)
        return df_renamed

    # 3. Feuilles de match
    # =================================
    @staticmethod
    def get_boxscore_by_game_id(game_id: str) -> DataFrame:
        """
        input : objet boxscoretraditionalv3
        Transformation en DataFrame, et renommage des colonnes.
        :return: DataFrame : Informations des boxscores.
        """
        try:
            raw_data = boxscoretraditionalv3.BoxScoreTraditionalV3(game_id=game_id)  # Appel API
        except Exception as e:
            print(f"Erreur lors de l'appel à BoxScoreTraditionalV3 avec game_id={game_id} : {e}")
            raw_data = None  # Valeur par défaut en cas d'échec

        df = Utils.obtenir_df_manipulable(raw_data)
        df_renamed = NbaApiColumnMapper.rename_columns_in_df(df, NbaApiEndpoints.BOX_SCORE_TRADITIONAL_V3.value)
        return df_renamed

    @staticmethod
    def get_scoreboardv2_by_game_date(game_date: date) -> tuple[DataFrame, DataFrame]:
        """
        input : objet scoreboardv2
        Transformation en DataFrame, renommage des colonnes, et conversion des dates.
        :return: DataFrame : Informations des matchs.
        """
        try:
            # Appel à l'API ScoreboardV2 pour obtenir les données des matchs du jour
            raw_data = scoreboardv2.ScoreboardV2(game_date=game_date)
        except Exception as e:
            # En cas d'échec de l'appel API, afficher l'erreur et retourner None
            print(f"Erreur lors de l'appel à ScoreboardV2 avec game_date={game_date} : {e}")
            raw_data = None  # Valeur par défaut en cas d'échec

        # Obtention et transformation du dataframe contenant les informations des matchs
        df_game_header = Utils.obtenir_df_manipulable(raw_data)
        df_game_header_tmp = NbaApiColumnMapper.rename_columns_in_df(df_game_header,
                                                                     NbaApiEndpoints.SCORE_BOARD_V2.value)
        df_game_header_tmp["game_date"] = df_game_header_tmp["game_date"].apply(Utils.convert_to_date)

        # Sélection des colonnes nécessaires et ajout de colonnes pour les scores
        df_game_header_final = df_game_header_tmp[
            ["game_date", "game_id", "game_status_text", "home_team_id", "visitor_team_id"]].copy()
        df_game_header_final['home_team_score'] = None  # Initialisation des scores à None
        df_game_header_final['visitor_team_score'] = None  # Initialisation des scores à None

        # Obtention et transformation du dataframe contenant les scores des équipes
        df_line_score = Utils.obtenir_df_manipulable(raw_data, 1)
        df_line_score_final = NbaApiColumnMapper.rename_columns_in_df(df_line_score,
                                                                      NbaApiEndpoints.SCORE_BOARD_V2.value)
        df_line_score_final["game_date"] = df_line_score_final["game_date"].apply(Utils.convert_to_date)

        # Fonction pour récupérer le score d'une équipe en fonction de son team_id
        def get_team_score(team_id, df_line_score_tmp):
            team_row = df_line_score_tmp[
                df_line_score_tmp['team_id'] == team_id]  # Filtre des lignes correspondant à l'équipe
            if not team_row.empty:
                return team_row['pts'].values[0]  # Récupère le score de l'équipe
            return None  # Retourne None si aucune donnée n'est trouvée

        # Mise à jour des scores pour chaque équipe dans df_game_header_final
        for index, row in df_game_header_final.iterrows():
            home_team_id = row['home_team_id']  # ID de l'équipe à domicile
            home_team_score = get_team_score(home_team_id,
                                             df_line_score_final)  # Récupère le score de l'équipe à domicile
            if home_team_score is not None:
                df_game_header_final.loc[index, 'home_team_score'] = home_team_score  # Mise à jour du score à domicile

            visitor_team_id = row['visitor_team_id']  # ID de l'équipe visiteuse
            visitor_team_score = get_team_score(visitor_team_id,
                                                df_line_score_final)  # Récupère le score de l'équipe visiteuse
            if visitor_team_score is not None:
                df_game_header_final.loc[
                    index, 'visitor_team_score'] = visitor_team_score  # Mise à jour du score visiteur

        # Retourne le DataFrame avec les informations des matchs et les scores
        return df_game_header_final


if __name__ == "__main__":
    # data = NbaApiService.get_common_player_info(2544)
    # data = NbaApiService.get_teams()
    # data = NbaApiService.get_boxscore_by_game_id("0022400629")
    # data = NbaApiService.get_team_roster_by_team_id(1610612747)
    # data = NbaApiService.get_team_game_log_by_team_id(1610612747)
    # data = NbaApiService.get_player_game_log_by_player_id(2544)
    # data = NbaApiService.get_player_next_games_by_player_id(2544)
    data = NbaApiService.get_scoreboardv2_by_game_date(date(2025, 1, 25))
    # data = NbaApiService.get_boxscore_by_game_id("0022400001")
    print("")

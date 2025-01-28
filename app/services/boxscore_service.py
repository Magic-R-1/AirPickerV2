import pandas as pd

from app.services.nba_api_service import NbaApiService


class BoxscoreService:

    def __init__(self):
        pass

    @staticmethod
    def get_df_boxscore_by_game_id(game_id: str) -> pd.DataFrame | None :
        """
        Utile la méthode de NbaApiService pour obtenir le DF de BoxScoreTraditionalV3

        :param game_id: L'identifiant unique du match.
        :return: Un DataFrame contenant les données du boxscore ou None en cas d'erreur.
        """
        try:
            return NbaApiService.get_boxscore_by_game_id(game_id)

        except Exception as e:
            print(f"Erreur lors de la récupération des données pour le boxscore {game_id}: {e}")
            return None


if __name__ == "__main__":
    df_boxscore = BoxscoreService.get_df_boxscore_by_game_id("1610612747")
    print("")
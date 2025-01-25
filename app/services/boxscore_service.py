from services.nba_api_service import NbaApiService
from utils.utils import Utils


class BoxscoreService:

    def __init__(self):
        pass

    @staticmethod
    def get_df_boxscore_by_game_id(game_id: str):
        boxscore_from_api = NbaApiService.get_boxscore_by_game_id(game_id)
        return Utils.obtenir_df_manipulable(boxscore_from_api)

if __name__ == "__main__":
    df_boxscore = BoxscoreService.get_df_boxscore_by_game_id("0022400596")
    print("")
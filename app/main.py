from app.dao.team_dao import TeamDAO
from app.services.nba_api_service import NbaApiService
from app.services.player_service import PlayerService
from dto.player_dto import PlayerDTO

def instancier_players():
    # Création d'instances de la classe Player
    player1 = PlayerDTO(player_id=1, first_name="LeBron", team_name="Lakers")
    player2 = PlayerDTO(player_id=2, first_name="Stephen", team_name="Warriors")

    # Affichage des informations sur les joueurs
    print(player1.first_name)
    print(player2.first_name)

if __name__ == "__main__":

    #player_id = PlayerService.get_player_dto_by_display_first_last("LeBron James").player_id
    list_past_games = NbaApiService.get_player_game_log_by_player_id(2544).get_data_frames()[0]
    list_game_id = list_past_games[["Game_ID"]]
    premier_id = list_game_id.iloc[0][0]
    boxscore = NbaApiService.get_boxscore_by_game_id(premier_id).get_data_frames()[0]

    print("toto")

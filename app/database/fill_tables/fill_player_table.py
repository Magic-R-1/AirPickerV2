from app.dao.player_dao import PlayerDAO
from app.services.nba_api_service import NbaApiService
from app.services.player_service import PlayerService

def fill_players_table():
    # Récupérer la liste des joueurs via l'API
    players_list = NbaApiService.get_players()[:2] # On récupère uniquement les 10 premiers joueurs pour tester

    for player in players_list:
        # Pour chaque joueur, obtenir plus d'informations à l'aide de CommonPlayerInfo
        person_id = player['id']
        player_info = NbaApiService.common_player_info_to_df(person_id)

        # Mapper les données de l'API vers PlayerDTO
        player_dto = PlayerService.map_common_player_info_to_player_dto(player_info)

        # Ajouter et valider l'entrée dans la base de données
        PlayerDAO.add_player(player_dto)

if __name__ == "__main__":
    fill_players_table()
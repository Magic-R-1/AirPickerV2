from app.services.api_service import ApiService

class PlayerService:

    def __init__(self):
        pass

    @staticmethod
    def get_player_id_by_name(player_name):

        player_list = ApiService.get_players()

        # Recherche du joueur par son nom
        player = next((player for player in player_list if player['full_name'] == player_name), None)

        if player:
            return player['id']
        else:
            raise ValueError(f"Le joueur '{player_name}' n'a pas été trouvé.")

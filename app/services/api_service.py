from nba_api.stats.static import players

class ApiService:
    def __init__(self):
        pass

    @staticmethod
    def get_players():
        # Utilisation de la fonction get_players de nba_api pour obtenir les joueurs
        return players.get_players()
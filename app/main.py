from app.services.player_service import PlayerService
from models.player import Player

def main():
    # Création d'instances de la classe Player
    player1 = Player(player_id=1, name="LeBron James", team="Los Angeles Lakers")
    player2 = Player(player_id=2, name="Stephen Curry", team="Golden State Warriors")

    # Affichage des informations sur les joueurs
    print(player1)
    print(player2)

    # Recherche de l'ID d'un joueur par son nom
    try:
        player_id = PlayerService.get_player_id_by_name("LeBron James")
        print(f"L'ID de LeBron James est {player_id}")
    except ValueError as e:
        print(e)

if __name__ == "__main__":
    main()

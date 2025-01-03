from models.player import Player
from models.team import Team

def main():
    # Création d'instances de la classe Player
    player1 = Player(id=1, name="LeBron James", team="Los Angeles Lakers")
    player2 = Player(id=2, name="Stephen Curry", team="Golden State Warriors")

    # Affichage des informations sur les joueurs
    print(player1)
    print(player2)

if __name__ == "__main__":
    main()

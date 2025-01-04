from app.services.player_service import PlayerService
from dto.player_dto import PlayerDTO

def instancier_players():
    # Création d'instances de la classe Player
    player1 = PlayerDTO(person_id=1, first_name="LeBron", team_name="Lakers")
    player2 = PlayerDTO(person_id=2, first_name="Stephen", team_name="Warriors")

    # Affichage des informations sur les joueurs
    print(player1.first_name)
    print(player2.first_name)

def main():

    # Recherche de l'ID d'un joueur par son nom
    try:
        player_id = PlayerService.get_player_id_by_name("LeBron James")
        print(f"L'ID de LeBron James est {player_id}")
    except ValueError as e:
        print(e)

if __name__ == "__main__":
    instancier_players()

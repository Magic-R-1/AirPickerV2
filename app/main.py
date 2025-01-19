from app.dao.team_dao import TeamDAO
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
    print("toto")

import time

from tqdm import tqdm
from app.database.db_connector import SessionLocal
from app.services.player_service import PlayerService

def fill_players_table():
    # Récupérer la liste des joueurs via l'API
    players_list = PlayerService.get_active_players()

    # Boucler sur ces joueurs en ajoutant leurs informations avec CommonPlayerInfo
    with SessionLocal() as db:
        try:
            # La barre de progression avec tqdm
            for i, player in tqdm(enumerate(players_list), desc="Ajout des joueurs", unit="joueur", total=len(players_list)):
                person_id = player['id']
                player_info = PlayerService.common_player_info_to_df(person_id)

                # Mapper les données de l'API vers PlayerDTO
                player_dto = PlayerService.map_common_player_info_to_player_dto(player_info)

                # Ajouter l'entrée à la session sans valider
                db.add(player_dto)

                # Ajouter une pause après chaque 100 joueurs
                if (i % 100 == 0) & (i!=0):
                    delai = 60
                    print(f"Pause de {delai} secondes après l'ajout de {i} joueurs...")
                    time.sleep(delai)  # Pause de {delai} secondes

            # Une seule validation à la fin de la boucle
            db.commit()
            print(f"Tous les {len(players_list)} joueurs ont été ajoutés à la base de données avec succès.")

        except Exception as e:
            db.rollback()  # Annuler en cas d'erreur
            print(f"Une erreur est survenue lors de l'ajout des joueurs : {e}")

if __name__ == "__main__":
    fill_players_table()

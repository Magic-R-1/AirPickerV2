import time
from tqdm import tqdm

from app.config import Config
from app.database.db_connector import engine, SessionLocal
from app.models.player import Player
from app.services.player_service import PlayerService


class PlayerTableLifeCycle:

    @staticmethod
    def create_player_table():
        # Base.metadata.create_all(engine) # Pour créer toutes les classes héritant de Base
        Player.__table__.create(engine)

        print("Table 'player' créée avec succès.")

    @staticmethod
    def fill_player_table():
        # Récupérer la liste des joueurs via l'API
        players_list = PlayerService.get_active_players()

        # Boucler sur ces joueurs en ajoutant leurs informations avec CommonPlayerInfo
        with SessionLocal() as db:
            try:
                # La barre de progression avec tqdm
                for i, player in tqdm(enumerate(players_list), desc="Ajout des joueurs", unit="joueur", total=len(players_list)):
                    person_id = player['id']
                    player_info = PlayerService.person_id_to_common_player_info_df(person_id)

                    # Mapper les données de l'API vers PlayerDTO
                    player_dto = PlayerService.map_common_player_info_to_player_dto(player_info)

                    # Ajouter l'entrée à la session sans valider
                    db.add(player_dto)

                    # Ajouter une pause après chaque x joueurs
                    if (i % Config.NBA_API_TEMPO_PLAYERS == 0) & (i!=0):
                        delai = Config.NBA_API_TEMPO
                        print(f"Pause de {delai} secondes après l'ajout de {i} joueurs...")
                        time.sleep(delai)  # Pause de x secondes

                db.commit()
                print(f"Tous les {len(players_list)} joueurs ont été ajoutés à la base de données avec succès.")

            except Exception as e:
                db.rollback()
                print(f"Une erreur est survenue lors de l'ajout des joueurs : {e}")

    @staticmethod
    def clear_player_table():
        with SessionLocal() as session:
            try:
                # Vider la table en supprimant tous les enregistrements
                session.query(Player).delete()
                session.commit()  # Valider les changements
                print("La table player a été vidée avec succès.")
            except Exception as e:
                session.rollback()  # Annuler en cas d'erreur
                print(f"Une erreur est survenue lors du vidage de la table player : {e}")

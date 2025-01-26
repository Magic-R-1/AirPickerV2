import time
from tqdm import tqdm

from config.config import Config
from app.dao.player_dao import PlayerDAO
from app.database.db_connector import engine, SessionLocal
from app.models.player import Player
from app.services.player_service import PlayerService


class PlayerTableMgmt:

    @staticmethod
    def create_player_table():
        Player.__table__.create(engine)
        print("Table 'player' créée avec succès.")

    @staticmethod
    def fill_player_table():
        # Récupérer la liste des joueurs via l'API
        players_list = PlayerService.get_list_active_players()

        # Diviser la liste en 2 pour éviter les erreurs de timeout de l'API NBA
        size = round(players_list.__sizeof__()/2,0)

        moitie = 1

        if moitie==1 :
            #players_list = PlayerService.get_active_players()[:size]
            # TODO : à enlever un jour
            players_list = PlayerService.get_list_active_players()[:90]
        elif moitie==2:
            players_list = PlayerService.get_list_active_players()[size:]

        # Boucler sur ces joueurs en ajoutant leurs informations avec CommonPlayerInfo
        with SessionLocal() as db:
            try:
                # La barre de progression avec tqdm
                for i, player in tqdm(
                        enumerate(players_list),
                        desc="Ajout des joueurs",
                        unit="joueur",
                        total=len(players_list)
                ):

                    # Récupérer le DataFrame commonplayerinfo depuis l'API
                    player_info = PlayerService.get_df_common_player_info_by_player_id(player['id'])

                    # Mapper les données de l'API vers Player model
                    player_sqlalchemy = PlayerService.map_common_player_info_to_player_model(player_info)

                    # Ajouter l'entrée à la session sans valider
                    db.add(player_sqlalchemy)

                    # Ajouter une pause après chaque x joueurs
                    if (i % Config.NBA_API_TEMPO_PLAYERS == 0) & (i!=0):
                        delai = Config.NBA_API_TEMPO
                        print(f"Pause de {delai} secondes après l'ajout de {i} joueurs.")
                        time.sleep(delai)  # Pause de x secondes

                db.commit()
                print(f"Tous les {len(players_list)} joueurs ont été ajoutés à la base de données avec succès.")

            except Exception as e:
                db.rollback()
                print(f"Une erreur est survenue lors de l'ajout des joueurs : {e}")

    @staticmethod
    def update_player_table():
        # TODO : Créer un DF avec ce qui est en base, un autre avec tous les joueurs de l'API, comparer les 2, et faire des updates depuis le DF API pour tout ce qui est différent
        print("")

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

    @staticmethod
    def drop_player_table():
        with SessionLocal() as session:
            try:
                # Supprimer la table Player
                Player.__table__.drop(bind=session.get_bind())
                print("La table player a été supprimée avec succès.")
            except Exception as e:
                print(f"Une erreur est survenue lors de la suppression de la table player : {e}")

if __name__ == "__main__":
    PlayerTableMgmt.fill_player_table()
import time
from tqdm import tqdm

from app.config.config import Config
from app.database.db_connector import engine, SessionLocal
from app.models.player import Player
from app.services.player_service import PlayerService
from app.services.nba_api_service import NbaApiService


class PlayerTableMgmt:

    @staticmethod
    def create_player_table():
        Player.__table__.create(engine)
        print("Table 'player' créée avec succès.")

    @staticmethod
    def fill_player_table():
        """
        Remplit la table des joueurs dans la base de données en récupérant les informations
        des joueurs actifs via l'API et en les ajoutant à la base de données.
        """
        # Récupérer la liste des joueurs actifs via PlayerService
        active_players_df = PlayerService.get_df_active_players_from_api()

        # Diviser le DataFrame en deux moitiés pour éviter les erreurs de timeout
        size = len(active_players_df) // 2

        # Choisir la moitié à traiter
        moitie = 2  # Modifier cette variable pour choisir la moitié
        if moitie == 1:
            #active_players_df = active_players_df.iloc[:90]  # Limitation temporaire, à remplacer par active_players_df = active_players_df.iloc[:size]
            active_players_df = active_players_df.iloc[:size]
        elif moitie == 2:
            active_players_df = active_players_df.iloc[size:]

        # Boucler sur les joueurs pour ajouter leurs informations
        with SessionLocal() as db:
            try:
                # Barre de progression avec tqdm
                for i, player in tqdm( # ne pas oublier l'index, qui évite de créer des tuples
                        enumerate(active_players_df.itertuples(index=False)),
                        desc="Ajout des joueurs",
                        unit="joueur",
                        total=len(active_players_df)
                ):
                    # Récupérer le DataFrame commonplayerinfo depuis l'API
                    player_info = NbaApiService.get_common_player_info(player.player_id)

                    # Mapper les données vers le modèle Player
                    player_sqlalchemy = PlayerService.map_common_player_info_df_to_player_model(player_info)

                    # Ajouter l'entrée à la session sans valider immédiatement
                    db.add(player_sqlalchemy)

                    # Pause après un certain nombre de joueurs pour éviter les limites de l'API
                    if (i % Config.NBA_API_TEMPO_PLAYERS == 0) and (i != 0):
                        delai = Config.NBA_API_TEMPO
                        print(f" Pause de {delai} secondes après l'ajout de {i} joueurs.")
                        time.sleep(delai)

                db.commit()
                print(f"Tous les {len(active_players_df)} joueurs ont été ajoutés à la base de données avec succès.")

            except Exception as e:
                db.rollback()
                print(f"Une erreur est survenue lors de l'ajout des joueurs : {e}")

    @staticmethod
    # TODO
    def update_player_table():
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
    #PlayerTableMgmt.clear_player_table()
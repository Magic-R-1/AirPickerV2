import time
from tqdm import tqdm

from app.config import Config
from app.database.db_connector import SessionLocal, engine
from app.dto.player_dto import PlayerDTO
from app.models.player import Player
from app.services.player_service import PlayerService


class PlayerDAO:

    # 1. CRUD
    # =================================

    @staticmethod
    def add_player(player_data):
        with SessionLocal() as session:
            session.add(player_data)
            session.commit()
            session.refresh(player_data)
            return player_data

    @staticmethod
    def get_player_by_id(player_id: int):
        with SessionLocal() as session:
            return session.query(Player).filter_by(person_id=player_id).first()

    @staticmethod
    def get_all_players():
        with SessionLocal() as session:
            return session.query(Player).all()

    @staticmethod
    def update_player(player_dto: PlayerDTO):
        """
        Met à jour les informations d'un joueur en base de données à partir d'un PlayerDTO.
        :param player_dto: Un objet PlayerDTO contenant les nouvelles informations du joueur.
        """
        with SessionLocal() as session:
            try:
                # Récupérer le joueur à mettre à jour à partir du modèle SQLAlchemy Player
                player_from_sqlalchemy = session.query(Player).filter_by(person_id=player_dto.person_id).first()

                if player_from_sqlalchemy is None:
                    print(f"Aucun joueur trouvé avec person_id = {player_dto.person_id}")
                    return

                # Mettre à jour les champs du joueur
                for field, value in vars(player_dto).items():
                    if hasattr(player_from_sqlalchemy, field) and value is not None:
                        setattr(player_from_sqlalchemy, field, value)

                # Valider les modifications
                session.flush()
                session.commit()

                print(f"Les informations du joueur {player_dto.person_id} ont été mises à jour avec succès.")
            except Exception as e:
                session.rollback()
                print(f"Une erreur est survenue lors de la mise à jour du joueur : {e}")

    @staticmethod
    def delete_player(player_id: int):
        with SessionLocal() as session:
            player = session.query(Player).filter_by(person_id=player_id).first()
            if player:
                session.delete(player)
                session.commit()
                return True
            return False

    # 2. Utils
    # =================================

    @staticmethod
    def player_from_sqlalchemy_to_dto(sqlalchemy_obj):
        """
        Convertit un objet SQLAlchemy en une instance de PlayerDTO de manière dynamique.
        :param sqlalchemy_obj: Objet SQLAlchemy (ex: Player)
        :return: Une instance de PlayerDTO
        """
        # Utilisation de __dict__ pour récupérer tous les attributs de l'objet SQLAlchemy
        # On filtre les éléments qui commencent par '_' (attributs internes à SQLAlchemy)
        attributes = {key: value for key, value in sqlalchemy_obj.__dict__.items() if not key.startswith('_')}

        # Créer une instance de PlayerDTO avec ces attributs
        return PlayerDTO(**attributes)

    # 3. Table lifecycle
    # =================================

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
                    player_info = PlayerService.common_player_info_to_df(person_id)

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

if __name__ == "__main__":

    player = PlayerDTO(person_id=201587, first_name="Nicolas", last_name="Batum")
    PlayerDAO.update_player(player)

    #player_sqlalchemy = PlayerDAO.get_player_by_id(201587)
    #player_dto = PlayerDAO.player_from_sqlalchemy_to_dto(player_sqlalchemy)
    #print(player_dto)

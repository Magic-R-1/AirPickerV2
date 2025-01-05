from app.database.db_connector import SessionLocal, engine
from app.dto.player_dto import PlayerDTO
from app.exceptions.exceptions import PlayerNotFoundError
from app.models.player import Player


class PlayerDAO:

    # 1. CRUD
    # =================================

    @staticmethod
    def add_player(player_dto: PlayerDTO):
        try:
            # Convertir le PlayerDTO en objet Player
            player_to_sqlalchemy = PlayerDAO.player_dto_to_sqlalchemy(player_dto)

            # Ajouter l'objet Player à la session SQLAlchemy
            with SessionLocal() as session:
                session.add(player_to_sqlalchemy)
                session.commit()
                session.refresh(player_to_sqlalchemy)
                return player_to_sqlalchemy  # Retourner l'objet Player nouvellement ajouté

        except Exception as e:
            print(f"Erreur lors de l'ajout du joueur: {e}")
            return None

    @staticmethod
    def get_player_by_id(player_id: int):
        with SessionLocal() as session:
            player_from_sqlalchemy = session.query(Player).filter_by(person_id=player_id).first()
            if player_from_sqlalchemy is None:
                raise PlayerNotFoundError(f"Joueur avec l'id '{player_id}' non trouvé.")
            return player_from_sqlalchemy

    @staticmethod
    def get_player_by_display_first_last(display_first_last: str):
        with SessionLocal() as session:
            player_from_sqlalchemy = session.query(Player).filter_by(display_first_last=display_first_last).all()
            if not player_from_sqlalchemy: # Aucun joueur trouvé
                raise PlayerNotFoundError(f"Joueur avec display_first_last '{display_first_last}' non trouvé.")
            elif len(player_from_sqlalchemy) == 1:  # Un joueur trouvé
                player_from_sqlalchemy = player_from_sqlalchemy[0]
            else: # Plusieurs joueurs trouvés
                raise ValueError(f"Plusieurs joueurs trouvés pour le nom '{display_first_last}.")
            return player_from_sqlalchemy

    @staticmethod
    def get_all_players():
        with SessionLocal() as session:
            players_from_sqlalchemy = session.query(Player).all()
            if players_from_sqlalchemy is None:
                raise PlayerNotFoundError(f"Aucun joueur trouvé.")
            return players_from_sqlalchemy

    @staticmethod
    def update_player(player_dto: PlayerDTO):
        """
        Met à jour les informations d'un joueur en base de données à partir d'un PlayerDTO.
        :param player_dto: Un objet PlayerDTO contenant les nouvelles informations du joueur.
        """
        with SessionLocal() as session:
            try:
                player_from_sqlalchemy = session.query(Player).filter_by(person_id=player_dto.person_id).first()
                if player_from_sqlalchemy is None:
                    print(f"Aucun joueur trouvé avec person_id = {player_dto.person_id}")
                    return None

                # Mettre à jour directement les champs
                for field, value in vars(player_dto).items():
                    if hasattr(player_from_sqlalchemy, field) and value is not None:
                        setattr(player_from_sqlalchemy, field, value)

                # Valider les modifications
                session.commit()
                print(f"Les informations du joueur {player_dto.person_id} ont été mises à jour avec succès.")
                return player_from_sqlalchemy

            except Exception as e:
                session.rollback()
                print(f"Une erreur est survenue lors de la mise à jour du joueur : {e}")
                return None

    @staticmethod
    def delete_player(player_id: int):
        try:
            with SessionLocal() as session:
                player_from_sqlalchemy = session.query(Player).filter_by(person_id=player_id).first()
                if player_from_sqlalchemy:
                    session.delete(player_from_sqlalchemy)
                    session.commit()
                    return True
                else:
                    print(f"Aucun joueur trouvé avec l'ID: {player_id}")
                    return False
        except Exception as e:  # Capture toutes les exceptions générales
            print(f"Erreur lors de la suppression du joueur avec ID {player_id}: {e}")
            return False

    # 2. Utils
    # =================================

    @staticmethod
    def players_from_sqlalchemy_to_dto(sqlalchemy_obj):
        """
        Convertit un objet ou une liste d'objets SQLAlchemy en une ou plusieurs instances de PlayerDTO.
        :param sqlalchemy_obj: Un objet ou une liste d'objets SQLAlchemy.
        :return: Une instance ou une liste d'instances de PlayerDTO.
        """
        def convert_to_dto(obj):
            """ Convertit un seul objet SQLAlchemy en PlayerDTO """
            attributes = {key: value for key, value in vars(obj).items() if not key.startswith('_')}
            return PlayerDTO(**attributes)

        # Si l'argument est une liste, on parcourt chaque élément et on les convertit
        if isinstance(sqlalchemy_obj, list):
            return [convert_to_dto(obj) for obj in sqlalchemy_obj]

        # Si c'est un seul objet, on le convertit directement en PlayerDTO
        return convert_to_dto(sqlalchemy_obj)


    @staticmethod
    def player_dto_to_sqlalchemy(player_dto):
        if isinstance(player_dto, list):
            # Si l'entrée est une liste, on la convertit en une liste d'objets Player
            return [Player(**{k: v for k, v in vars(p).items() if hasattr(Player, k)}) for p in player_dto]
        else:
            # Si l'entrée est un seul objet, on le convertit directement
            return Player(**{k: v for k, v in vars(player_dto).items() if hasattr(Player, k)})

if __name__ == "__main__":

    #player = PlayerDTO(person_id=201587, first_name="Nicolas", last_name="Batum")
    #PlayerDAO.update_player(player)

    player = PlayerDTO(person_id=1, first_name="Erwan", last_name="Gretillat")
    PlayerDAO.delete_player(1)

    #player_sqlalchemy = PlayerDAO.get_player_by_id(201587)
    #player_dto = PlayerDAO.player_from_sqlalchemy_to_dto(player_sqlalchemy)
    #print(player_dto)

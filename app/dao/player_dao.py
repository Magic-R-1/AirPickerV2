from app.database.db_connector import session_scope
from app.dto.player_dto import PlayerDTO
from app.exceptions.exceptions import PlayerNotFoundError
from app.models.player import Player
from app.schemas.player_schema import PlayerSchema


class PlayerDAO:

    # 1. CRUD
    # =================================

    @staticmethod
    def add_player(player_dto: PlayerDTO):
        try:
            # Convertir le PlayerDTO en objet Player
            player_sqlalchemy = PlayerDAO.player_from_dto_to_sql(player_dto)

            # Ajouter l'objet Player à la session SQLAlchemy
            with session_scope() as session:
                session.add(player_sqlalchemy)
                session.commit()
                session.refresh(player_sqlalchemy)
                return player_sqlalchemy  # Retourner l'objet Player nouvellement ajouté

        except Exception as e:
            print(f"Erreur lors de l'ajout du joueur: {e}")
            return None

    @staticmethod
    def get_player_by_id(player_id: int):
        with session_scope() as session:
            player_from_sql = session.query(Player).filter_by(person_id=player_id).first()
            if player_from_sql is None:
                raise PlayerNotFoundError(f"Joueur avec l'id '{player_id}' non trouvé.")
            return player_from_sql

    @staticmethod
    def get_player_by_display_first_last(display_first_last: str):
        with session_scope() as session:
            player_from_sql = session.query(Player).filter_by(display_first_last=display_first_last).all()
            if not player_from_sql: # Aucun joueur trouvé
                raise PlayerNotFoundError(f"Joueur avec display_first_last '{display_first_last}' non trouvé.")
            elif len(player_from_sql) == 1:  # Un joueur trouvé
                player_from_sql = player_from_sql[0]
            else: # Plusieurs joueurs trouvés
                raise ValueError(f"Plusieurs joueurs trouvés pour le nom '{display_first_last}.")
            return player_from_sql

    @staticmethod
    def get_all_players():
        with session_scope() as session:
            players_from_sqlalchemy = session.query(Player).all()
            if players_from_sqlalchemy is None:
                raise PlayerNotFoundError(f"Aucun joueur trouvé.")
            return players_from_sqlalchemy

    @staticmethod
    def update_player(player_dto: PlayerDTO):
        """
        Met à jour les informations d'un joueur en base de données à partir d'un PlayerDTO.

        :param player_dto: Un objet PlayerDTO contenant les nouvelles informations du joueur.
        :return: L'instance mise à jour de Player ou None si le joueur n'a pas été trouvé.
        """
        with session_scope() as session:
            try:
                # Récupérer le joueur en base
                player_from_sql = session.query(Player).filter_by(person_id=player_dto.person_id).first()

                if player_from_sql is None:
                    print(f"Aucun joueur trouvé avec person_id = {player_dto.person_id}")
                    return None

                # Mise à jour des champs valides
                player_schema = PlayerSchema().dump(player_dto)
                for field, value in player_schema.items():
                    if hasattr(player_from_sql, field):
                        setattr(player_from_sql, field, value)

                # Valider les modifications
                session.commit()
                print(f"Les informations du joueur {player_dto.person_id} ont été mises à jour avec succès.")
                return player_from_sql

            except Exception as e:
                session.rollback()
                print(f"Une erreur est survenue lors de la mise à jour du joueur : {e}")
                return None

    @staticmethod
    def delete_player_by_id(player_id: int):
        try:
            with session_scope() as session:
                player_from_sql = session.query(Player).filter_by(person_id=player_id).first()
                if player_from_sql:
                    session.delete(player_from_sql)
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
    def player_from_dto_to_sql(player_dto: PlayerDTO):
        """
        Convertit une instance PlayerDTO en une instance SQLAlchemy Player en passant par PlayerSchema.

        :param player_dto: Instance de PlayerDTO contenant les données.
        :return: Instance SQLAlchemy du modèle Player.
        """
        # Convertir PlayerDTO en dictionnaire
        player_schema = PlayerSchema().dump(player_dto)
        # Créer une instance SQLAlchemy Player
        return Player(**player_schema)

    @staticmethod
    def player_from_sql_to_dto(player_sqlalchemy: Player):
        """
        Convertit une instance SQLAlchemy Player en une instance PlayerDTO.

        :param player_sqlalchemy: Instance SQLAlchemy du modèle Player.
        :return: Instance de PlayerDTO.
        """
        # Sérialisation avec Marshmallow
        player_data = PlayerSchema().dump(player_sqlalchemy)
        # Création de l'instance PlayerDTO
        return PlayerDTO(**player_data)

if __name__ == "__main__":

    #player = PlayerDTO(person_id=201587, first_name="Nicolas", last_name="Batum")
    #PlayerDAO.update_player(player)

    #player_dto = PlayerDTO(person_id=1, first_name="Erwan", last_name="Gretillat")
    #player_sqlalchemy = PlayerDAO.player_from_dto_to_sql(player_dto)
    #PlayerDAO.add_player(player_dto)
    PlayerDAO.delete_player_by_id(1)

    #player_sql = PlayerDAO.get_player_by_id(2544)
    #player_dto = PlayerDAO.player_from_sql_to_dto(player_sql)
    #print(player_dto)

from app.dto.player_dto import PlayerDTO
from app.database.db_connector import SessionLocal
from app.models.player import Player

class PlayerDAO:

    @staticmethod
    def get_player_by_id(player_id: int):
        with SessionLocal() as session:
            return session.query(Player).filter_by(person_id=player_id).first()

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

    @staticmethod
    def add_player(player_data):
        with SessionLocal() as session:
            session.add(player_data)
            session.commit()
            session.refresh(player_data)
            return player_data

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
                        print(f"Mise à jour du champ {field} avec la valeur {value}")
                        setattr(player_from_sqlalchemy, field, value)

                # Vérifier les modifications sur l'objet player avant commit
                player_from_sqlalchemy_to_dto = PlayerDAO.player_from_sqlalchemy_to_dto(player_from_sqlalchemy)
                print(f"Joueur modifié avant commit: {player_from_sqlalchemy_to_dto}")

                # Valider les modifications
                session.commit()  # Utiliser commit pour valider définitivement

                # Récupérer les informations après commit pour confirmer les changements
                updated_player = session.query(Player).filter_by(person_id=player_dto.person_id).first()
                updated_player_dto = PlayerDAO.player_from_sqlalchemy_to_dto(updated_player)
                print(f"Joueur mis à jour après commit: {updated_player_dto}")

                print(f"Les informations du joueur {player_dto.person_id} ont été mises à jour avec succès.")
            except Exception as e:
                session.rollback()
                print(f"Une erreur est survenue lors de la mise à jour du joueur : {e}")

    @staticmethod
    def get_all_players():
        with SessionLocal() as session:
            return session.query(Player).all()

    @staticmethod
    def delete_player(player_id: int):
        with SessionLocal() as session:
            player = session.query(Player).filter_by(person_id=player_id).first()
            if player:
                session.delete(player)
                session.commit()
                return True
            return False

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

    player = PlayerDTO(person_id=201587, first_name="Nicolasse", last_name="Batume")
    PlayerDAO.update_player(player)

    #player_sqlalchemy = PlayerDAO.get_player_by_id(201587)
    #player_dto = PlayerDAO.player_from_sqlalchemy_to_dto(player_sqlalchemy)
    #print(player_dto)

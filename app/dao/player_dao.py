from app.dto.player_dto import PlayerDTO
from app.database.db_connector import SessionLocal

class PlayerDAO:

    @staticmethod
    def get_player_by_id(player_id: int):
        with SessionLocal() as db:
            return db.query(PlayerDTO).filter_by(person_id=player_id).first()

    @staticmethod
    def add_player(player_data):
        with SessionLocal() as db:
            db.add(player_data)
            db.commit()
            db.refresh(player_data)
            return player_data

    @staticmethod
    def get_all_players():
        with SessionLocal() as db:
            return db.query(PlayerDTO).all()

    @staticmethod
    def delete_player(player_id: int):
        with SessionLocal() as db:
            player = db.query(PlayerDTO).filter_by(person_id=player_id).first()
            if player:
                db.delete(player)
                db.commit()
                return True
            return False

    @staticmethod
    def clear_player_table():
        with SessionLocal() as db:
            try:
                # Vider la table en supprimant tous les enregistrements
                db.query(PlayerDTO).delete()
                db.commit()  # Valider les changements
                print("La table player a été vidée avec succès.")
            except Exception as e:
                db.rollback()  # Annuler en cas d'erreur
                print(f"Une erreur est survenue lors du vidage de la table player : {e}")

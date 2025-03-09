from typing import List

import pandas as pd

from app.database.db_connector import session_scope
from app.dto.player_dto import PlayerDTO
from app.exceptions.exceptions import PlayerNotFoundError
from app.models.player import Player
from app.schemas.player_schema import PlayerSchema
from app.services.nba_api_service import NbaApiService


class PlayerDAO:

    # 1. CRUD
    # =================================

    @staticmethod
    def add_player(player_dto: PlayerDTO) -> bool:
        try:
            # Convertir le PlayerDTO en objet Player
            player_sqlalchemy = PlayerDAO.player_from_dto_to_sql(player_dto)

            # Ajouter l'objet Player à la session SQLAlchemy
            with session_scope() as session:
                session.add(player_sqlalchemy)
                session.commit()
                session.refresh(player_sqlalchemy)
                print(f"Player ajouté : {player_dto.display_first_last}")
                return True

        except Exception as e:
            print(f"Erreur lors de l'ajout du joueur : {e}")
            return False

    @staticmethod
    def add_player_from_player_id(player_id: int) -> bool:
        player = NbaApiService.get_common_player_info(player_id)
        player_dto = PlayerDAO.player_from_commonplayerinfo_to_dto(player)
        return PlayerDAO.add_player(player_dto)

    @staticmethod
    def get_player_by_id(player_id: int) -> Player:
        with session_scope() as session:
            player_sqlalchemy = session.query(Player).filter_by(player_id=player_id).first()
            if player_sqlalchemy is None:
                raise PlayerNotFoundError(f"Joueur avec l'id '{player_id}' non trouvé.")
            return player_sqlalchemy

    @staticmethod
    def get_player_by_display_first_last(display_first_last: str) -> Player:
        with session_scope() as session:
            player_sqlalchemy = session.query(Player).filter_by(display_first_last=display_first_last).all()
            if not player_sqlalchemy:  # Aucun joueur trouvé
                raise PlayerNotFoundError(f"Joueur avec display_first_last '{display_first_last}' non trouvé.")
            elif len(player_sqlalchemy) == 1:  # Un joueur trouvé
                player_sqlalchemy = player_sqlalchemy[0]
            else:  # Plusieurs joueurs trouvés
                raise ValueError(f"Plusieurs joueurs trouvés pour le nom '{display_first_last}.")
            return player_sqlalchemy

    @staticmethod
    def get_all_players() -> List[Player]:
        with session_scope() as session:
            players_from_sqlalchemy = session.query(Player).all()
            if players_from_sqlalchemy is None:
                raise PlayerNotFoundError(f"Aucun joueur trouvé.")
            return players_from_sqlalchemy

    @staticmethod
    def update_player(player_dto: PlayerDTO) -> Player | None:
        """
        Met à jour les informations d'un joueur en base de données à partir d'un PlayerDTO.
        Méthode non-destructive : les champs existants non spécifiés dans l'input restent inchangés.

        :param player_dto: Un objet PlayerDTO contenant les nouvelles informations du joueur.
        :return: L'instance mise à jour de Player ou None si le joueur n'a pas été trouvé.
        """
        with session_scope() as session:
            try:
                # Récupérer le joueur en base
                player_sqlalchemy = session.query(Player).filter_by(player_id=player_dto.player_id).first()

                if player_sqlalchemy is None:
                    print(f"Aucun joueur trouvé avec player_id = {player_dto.player_id}")
                    return None

                # Mise à jour des champs valides
                player_schema = PlayerSchema().dump(player_dto)
                for field, value in player_schema.items():
                    if hasattr(player_sqlalchemy, field):
                        setattr(player_sqlalchemy, field, value)

                # Valider les modifications
                session.commit()
                print(f"Les informations du joueur {player_dto.player_id} ont été mises à jour avec succès.")
                return player_sqlalchemy

            except Exception as e:
                session.rollback()
                print(f"Une erreur est survenue lors de la mise à jour du joueur : {e}")
                return None

    @staticmethod
    def delete_player_by_id(player_id: int) -> bool:
        try:
            with session_scope() as session:
                player_sqlalchemy = session.query(Player).filter_by(player_id=player_id).first()
                if player_sqlalchemy:
                    session.delete(player_sqlalchemy)
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
    def player_from_dto_to_sql(player_dto: PlayerDTO) -> Player:
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
    def player_from_sql_to_dto(player_sqlalchemy: Player) -> PlayerDTO:
        """
        Convertit une instance SQLAlchemy Player en une instance PlayerDTO.

        :param player_sqlalchemy: Instance SQLAlchemy du modèle Player.
        :return: Instance de PlayerDTO.
        """
        # Sérialisation avec Marshmallow
        player_schema = PlayerSchema().dump(player_sqlalchemy)
        # Création de l'instance PlayerDTO
        return PlayerDTO(**player_schema)

    @staticmethod
    def player_from_commonplayerinfo_to_dto(player_df: pd.DataFrame) -> PlayerDTO:
        player_dict = player_df.to_dict(orient="records")[0]

        player_schema = PlayerSchema().load(player_dict)
        player_model = Player(**player_schema)

        return player_model


if __name__ == "__main__":
    PlayerDAO.add_player_from_player_id(1641936)
    print()

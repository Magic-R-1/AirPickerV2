import pandas as pd

from app.dto.player_dto import PlayerDTO
from app.dao.player_dao import PlayerDAO
from app.exceptions.exceptions import PlayerNotFoundError
from app.schemas.player_schema import PlayerSchema
from app.services.nba_api_service import NbaApiService
from app.models.player import Player


class PlayerService:

    def __init__(self):
        pass

    @staticmethod
    def get_player_dto_by_display_first_last(player_name: str):

        try:
            player_sql = PlayerDAO.get_player_by_display_first_last(player_name)
        except (PlayerNotFoundError, ValueError) as e:
            print(f"Erreur: {e}")
            return None

        player_dto = PlayerDAO.player_from_sql_to_dto(player_sql)

        return player_dto

    @staticmethod
    def map_common_player_info_df_to_player_model(player_df):
        """
        Convertit les données de l'API NBA en Player en utilisant PlayerSchema.

        :param player_df: DataFrame contenant les données du joueur.
        :return: Instance de Player.
        """
        try:
            # Convertir la première (et seul) ligne du DataFrame en dictionnaire
            player_dict = player_df.iloc[0].to_dict()

            # Utilisation de PlayerSchema pour valider et structurer les données
            player_schema = PlayerSchema().load(player_dict)

            # Création de Player à partir des données validées
            return Player(**player_schema)

        except Exception as e:
            print(f"Erreur lors du mapping des données du joueur : {e}")
            return None

    @staticmethod
    def map_common_player_info_df_to_player_dto(player_df):
        """
        Convertit les données de l'API NBA en PlayerDTO en utilisant PlayerSchema.

        :param player_df: DataFrame contenant les données de l'API NBA.
        :return: Instance de PlayerDTO.
        """
        try:
            # Convertir la première (et seul) ligne du DataFrame en dictionnaire
            player_dict = player_df.iloc[0].to_dict()

            # Utilisation de PlayerSchema pour valider et structurer les données
            player_schema = PlayerSchema().load(player_dict)  # Valide et prépare les données

            # Création de PlayerDTO à partir des données validées
            return PlayerDTO(**player_schema)

        except Exception as e:
            print(f"Erreur lors du mapping des données du joueur : {e}")
            return None

    @staticmethod
    def get_df_active_players_from_api():

        df_players = NbaApiService.get_players()
        df_filtered = df_players[df_players['is_active']]

        return df_filtered

    @staticmethod
    def get_df_all_players_from_base() -> pd.DataFrame:

        players_from_sql = PlayerDAO.get_all_players()

        # Utilisation de la méthode `__dict__` pour obtenir les attributs des objets en dictionnaire
        players_dict = [player.__dict__ for player in players_from_sql]

        # Convertir la liste de dictionnaires en DataFrame
        df_players = pd.DataFrame(players_dict)

        # Supprimer la colonne '__table__' ajoutée par SQLAlchemy pour l'auto-référence
        if '_sa_instance_state' in df_players.columns:
            df_players.drop('_sa_instance_state', axis=1, inplace=True)

        return df_players


if __name__ == "__main__":
    print("")

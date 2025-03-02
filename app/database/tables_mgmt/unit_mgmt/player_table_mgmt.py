import time

import pandas as pd
from tqdm import tqdm

from app.config.config import Config
from app.database.db_connector import engine, SessionLocal
from app.models.player import Player
from app.services.player_service import PlayerService
from app.services.nba_api_service import NbaApiService
from utils.utils import Utils


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

        # PlayerTableMgmt.update_player_table()
        # TODO : à virer lorsque ça sera testé

        # Récupérer la liste des joueurs actifs via PlayerService
        active_players_df = PlayerService.get_df_active_players_from_api()

        # Diviser le DataFrame en deux moitiés pour éviter les erreurs de timeout
        size = len(active_players_df) // 2

        # Choisir la moitié à traiter
        moitie = 2  # Modifier cette variable pour choisir la moitié
        if moitie == 1:
            # active_players_df = active_players_df.iloc[:90]  # Limitation temporaire, à remplacer par active_players_df = active_players_df.iloc[:size]
            active_players_df = active_players_df.iloc[:size]
        elif moitie == 2:
            active_players_df = active_players_df.iloc[size:]

        # Boucler sur les joueurs pour ajouter leurs informations
        with SessionLocal() as db:
            try:
                # Barre de progression avec tqdm
                for i, player in tqdm(  # ne pas oublier l'index, qui évite de créer des tuples
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
    def update_player_table_old():

        df_players_from_base = PlayerService.get_df_all_players_from_base()
        df_active_players_from_api = PlayerService.get_df_active_players_from_api()

        list_populated_players_from_api = []

        df_active_players_from_api = df_active_players_from_api.iloc[:5]

        # Barre de progression avec tqdm
        for i, row in tqdm(
                enumerate(df_active_players_from_api.itertuples(index=False)),
                desc="Ajout des joueurs",
                unit="joueur",
                total=len(df_active_players_from_api)
        ):
            player_info = NbaApiService.get_common_player_info(row.player_id)
            # Ajout d'un DF player_info à une liste (plus rapide que de rajouter des lignes à un DF
            list_populated_players_from_api.append(player_info.to_dict(orient='records')[0])

            # Pause après un certain nombre de joueurs pour éviter les limites de l'API
            if (i % Config.NBA_API_TEMPO_PLAYERS == 0) and (i != 0):
                delai = Config.NBA_API_TEMPO
                print(f" Pause de {delai} secondes après l'ajout de {i} joueurs.")
                time.sleep(delai)

        # Conversion de la liste en DF
        df_populated_players_from_api = pd.DataFrame(list_populated_players_from_api)

        # Convertir des colonnes d'object à float64 (conversion initiale causée par l'utilisation d'une liste)
        df_populated_players_from_api['weight'] = pd.to_numeric(df_populated_players_from_api['weight'],
                                                                errors='coerce')
        df_populated_players_from_api['jersey_num'] = pd.to_numeric(df_populated_players_from_api['jersey_num'],
                                                                    errors='coerce')

        # Enlever la colonne team du DF provenant de la base
        df_players_from_base.drop(columns=['team'], inplace=True)

        # Changer les formats de la colonne birthdate de chaque DF
        df_populated_players_from_api['birthdate'] = pd.to_datetime(
            df_populated_players_from_api['birthdate']).dt.strftime('%Y-%m-%d')
        df_players_from_base['birthdate'] = pd.to_datetime(df_players_from_base['birthdate']).dt.strftime('%Y-%m-%d')

        # Fusionner les deux DF
        df_merge = df_populated_players_from_api.merge(df_players_from_base, how='outer',
                                                       indicator=True)

        # Garder seulement les lignes présentes dans df_populated_players_from_api mais pas dans df_players_from_base
        df_different_players_from_api = df_merge[
            df_merge['_merge'] == 'left_only'].drop(columns=['_merge'])

        # Filtrer df_different_players_from_api en excluant les player_id présents dans df_players_from_base
        df_players_to_add = df_different_players_from_api[
            ~df_different_players_from_api['player_id'].isin(df_players_from_base['player_id'])]

        # Filtrer df_different_players_from_api en incluant uniquement les player_id présents dans df_players_from_base
        df_players_to_update = df_different_players_from_api[
            df_different_players_from_api['player_id'].isin(df_players_from_base['player_id'])]

        try:
            with SessionLocal() as db:
                # Update
                for _, row in df_players_to_update.iterrows():
                    db.query(Player).filter(Player.player_id == row['player_id']).update(row.to_dict())

                # Ajout
                for _, row in df_players_to_add.iterrows():
                    # Convertir la ligne en DF
                    row_df = pd.DataFrame([row])

                    # Mapper les données vers le modèle Player
                    player_sqlalchemy = PlayerService.map_common_player_info_df_to_player_model(row_df)

                    # Ajouter l'entrée à la session sans valider immédiatement
                    db.add(player_sqlalchemy)

                db.flush()
                db.commit()

                count_update = len(df_players_to_update)
                count_ajout = len(df_players_to_add)
                print(f" Update de {count_update} joueurs.")
                print(f" Ajout de {count_ajout} joueurs.")

        except Exception as e:
            db.rollback()
            print(f"Une erreur est survenue lors de la mise à jour des joueurs : {e}")

    @staticmethod
    def update_player_table():
        # Récupérer les données
        df_players_from_base = PlayerService.get_df_all_players_from_base()
        df_active_players_from_api = PlayerService.get_df_active_players_from_api()

        # Traitement des joueurs actifs
        df_populated_players_from_api = PlayerTableMgmt.update_populate_active_players(df_active_players_from_api)

        # Conversion et préparation des DataFrames
        PlayerTableMgmt.update_prepare_df(df_players_from_base, df_populated_players_from_api)

        # Fusionner et filtrer les DataFrames
        df_players_to_add, df_players_to_update = PlayerTableMgmt.update_merge_and_filter_players(df_players_from_base,
                                                                                                  df_populated_players_from_api)

        # Mettre à jour la base de données
        PlayerTableMgmt.update_write_in_database(df_players_to_add, df_players_to_update)

    @staticmethod
    def update_populate_active_players(df_active_players_from_api):
        list_populated_players_from_api = []

        # Limiter à 5 joueurs
        # df_active_players_from_api = df_active_players_from_api.iloc[:5]

        for i, row in tqdm(
                enumerate(df_active_players_from_api.itertuples(index=False)),
                desc="Ajout des joueurs",
                unit="joueur",
                total=len(df_active_players_from_api)
        ):
            player_info = NbaApiService.get_common_player_info(row.player_id)
            list_populated_players_from_api.append(player_info.to_dict(orient='records')[0])

            # Pause pour respecter les limites de l'API
            if (i % Config.NBA_API_TEMPO_PLAYERS == 0) and (i != 0):
                print(f" Pause de {Config.NBA_API_TEMPO} secondes après l'ajout de {i} joueurs.")
                time.sleep(Config.NBA_API_TEMPO)

        # Convertir la liste en DataFrame
        return pd.DataFrame(list_populated_players_from_api)

    @staticmethod
    def update_prepare_df(df_players_from_base, df_populated_players_from_api):

        #df_populated_players_from_api = Utils.obtenir_df_manipulable(df_populated_players_from_api)
        #df_players_from_base = Utils.obtenir_df_manipulable(df_players_from_base)

        # Conversion des colonnes en types appropriés
        df_populated_players_from_api['weight'] = pd.to_numeric(df_populated_players_from_api['weight'],
                                                                errors='coerce')
        df_populated_players_from_api['jersey_num'] = pd.to_numeric(df_populated_players_from_api['jersey_num'],
                                                                    errors='coerce')

        # Supprimer la colonne team du DataFrame provenant de la base
        df_players_from_base.drop(columns=['team'], inplace=True)

        # Convertir les dates de naissance
        df_populated_players_from_api['birthdate'] = pd.to_datetime(
            df_populated_players_from_api['birthdate']).dt.strftime('%Y-%m-%d')
        df_players_from_base['birthdate'] = pd.to_datetime(df_players_from_base['birthdate']).dt.strftime('%Y-%m-%d')

    @staticmethod
    def update_merge_and_filter_players(df_players_from_base, df_populated_players_from_api):
        df_merge = df_populated_players_from_api.merge(df_players_from_base, how='outer', indicator=True)

        # Récupérer les joueurs à ajouter et à mettre à jour
        df_different_players_from_api = df_merge[df_merge['_merge'] == 'left_only'].drop(columns=['_merge'])

        df_players_to_add = df_different_players_from_api[
            ~df_different_players_from_api['player_id'].isin(df_players_from_base['player_id'])]
        df_players_to_update = df_different_players_from_api[
            df_different_players_from_api['player_id'].isin(df_players_from_base['player_id'])]

        return df_players_to_add, df_players_to_update

    @staticmethod
    def update_write_in_database(df_players_to_add, df_players_to_update):
        try:
            with SessionLocal() as db:
                # Mise à jour des joueurs existants
                for _, row in df_players_to_update.iterrows():
                    # Remplacer les NaN par None avant la mise à jour
                    row_dict = row.to_dict()
                    row_dict = {key: (None if pd.isna(value) else value) for key, value in row_dict.items()}

                    # Mettre à jour la base de données avec les valeurs corrigées
                    db.query(Player).filter(Player.player_id == row['player_id']).update(row_dict)

                # Ajout des nouveaux joueurs
                for _, row in df_players_to_add.iterrows():
                    row_df = pd.DataFrame([row])
                    player_sqlalchemy = PlayerService.map_common_player_info_df_to_player_model(row_df)
                    db.add(player_sqlalchemy)

                db.flush()
                db.commit()

                print(f" Update de {len(df_players_to_update)} joueurs.")
                print(f" Ajout de {len(df_players_to_add)} joueurs.")
        except Exception as e:
            db.rollback()
            print(f"Une erreur est survenue lors de la mise à jour des joueurs : {e}")

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
    PlayerTableMgmt.update_player_table()
    # PlayerTableMgmt.clear_player_table()

import pandas as pd
from tqdm import tqdm

from app.database.db_connector import SessionLocal
from app.models import Player
from app.services.nba_api_service import NbaApiService
from app.services.player_service import PlayerService


class PlayerTableMgmtUpdate:

    @staticmethod
    def update_player_table():
        # Récupérer les données
        df_players_from_base = PlayerService.get_df_all_players_from_base()
        df_active_players_from_api = PlayerService.get_df_active_players_from_api()

        # Traitement des joueurs actifs
        df_populated_players_from_api = PlayerTableMgmtUpdate.populate_active_players(df_active_players_from_api)

        # Conversion et préparation des DataFrames
        PlayerTableMgmtUpdate.prepare_df(df_players_from_base, df_populated_players_from_api)

        # Fusionner et filtrer les DataFrames
        df_players_to_add, df_players_to_update = PlayerTableMgmtUpdate.merge_and_filter_players(
            df_players_from_base,
            df_populated_players_from_api)

        # Mettre à jour la base de données
        PlayerTableMgmtUpdate.write_in_database(df_players_to_add, df_players_to_update)

    @staticmethod
    def ajouter_joueurs_inactifs_erreur(df_active_players_from_api: pd.DataFrame):
        """
        Ajoute des joueurs à la liste de joueurs actifs
        Nécessaire pour éviter les erreurs sur les imports de boxscore (joueurs dans boxscore, mais inactif depuis l'API)
        """
        # À remplir avec les erreurs remontées d'update_boxscore_table
        list_id_joueur_erreur = [1626143, 1628365, 1628396, 1630623, 1630639, 1631123, 1631209, 1641772, 1641878,
                                 1641879, 1641936, 1642443, 1642484, 1642486, 203109, 203901, 203926, 202687]

        for id_player in list_id_joueur_erreur:
            df_active_players_from_api.loc[len(df_active_players_from_api)] = [id_player, "", "", "", True]

    @staticmethod
    def populate_active_players(df_active_players_from_api):
        list_populated_players_from_api = []

        PlayerTableMgmtUpdate.ajouter_joueurs_inactifs_erreur(df_active_players_from_api)

        for i, row in tqdm(
                enumerate(df_active_players_from_api.itertuples(index=False)),
                desc="Ajout des joueurs",
                unit="joueur",
                total=len(df_active_players_from_api)
        ):
            player_info = NbaApiService.get_common_player_info(row.player_id)
            list_populated_players_from_api.append(player_info.to_dict(orient='records')[0])

            # Pause pour respecter les limites de l'API
            # if (i % Config.NBA_API_TEMPO_PLAYERS == 0) and (i != 0):
            #    print(f" Pause de {Config.NBA_API_TEMPO} secondes après l'ajout de {i} joueurs.")
            #    time.sleep(Config.NBA_API_TEMPO)

        # Convertir la liste en DataFrame
        return pd.DataFrame(list_populated_players_from_api)

    @staticmethod
    def prepare_df(df_players_from_base, df_populated_players_from_api):

        # df_populated_players_from_api = Utils.obtenir_df_manipulable(df_populated_players_from_api)
        # df_players_from_base = Utils.obtenir_df_manipulable(df_players_from_base)

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
    def merge_and_filter_players(df_players_from_base, df_populated_players_from_api):
        df_merge = df_populated_players_from_api.merge(df_players_from_base, how='outer', indicator=True)

        # Récupérer les joueurs à ajouter et à mettre à jour
        df_different_players_from_api = df_merge[df_merge['_merge'] == 'left_only'].drop(columns=['_merge'])

        df_players_to_add = df_different_players_from_api[
            ~df_different_players_from_api['player_id'].isin(df_players_from_base['player_id'])]
        df_players_to_update = df_different_players_from_api[
            df_different_players_from_api['player_id'].isin(df_players_from_base['player_id'])]

        return df_players_to_add, df_players_to_update

    @staticmethod
    def write_in_database(df_players_to_add, df_players_to_update):
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


if __name__ == "__main__":
    PlayerTableMgmtUpdate.update_player_table()

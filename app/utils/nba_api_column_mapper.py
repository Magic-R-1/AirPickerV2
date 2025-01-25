import os
import json
import pandas as pd

from enums.nba_api_endpoints import NbaApiEndpoints
from services.player_service import PlayerService


class NbaApiColumnMapper:

    # Charger le chemin du fichier JSON une seule fois pour éviter de charger à chaque appel de méthode
    json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'config', 'nba_api_column_mapping.json')

    @staticmethod
    def _load_json():
        """Charge le fichier JSON."""
        try:
            with open(NbaApiColumnMapper.json_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"Le fichier JSON n'a pas été trouvé à l'emplacement : {NbaApiColumnMapper.json_path}")
        except json.JSONDecodeError:
            raise ValueError("Le fichier JSON est malformé.")

    @staticmethod
    def get_reference(field: str):
        """Retourne la référence d'un champ donné."""
        data = NbaApiColumnMapper._load_json()

        # Cherche dans les endpoints pour trouver la clé correspondante
        for key, value in data.items():
            endpoints = value.get('endpoints', {})
            for endpoint, endpoint_value in endpoints.items():
                if endpoint_value == field:  # Si la valeur dans endpoints correspond au field
                    return value.get('reference', None)
        return None

    @staticmethod
    def get_endpoints(field: str):
        """Retourne les endpoints associés à un champ donné."""
        data = NbaApiColumnMapper._load_json()

        # Cherche le champ dans les endpoints et retourne l'objet endpoints
        for key, value in data.items():
            if field in value.get('endpoints', {}).values():
                return value.get('endpoints', {})
        return {}

    @staticmethod
    def get_example(field: str):
        """Retourne un exemple de valeur pour un champ donné."""
        data = NbaApiColumnMapper._load_json()

        # Cherche le champ et retourne l'exemple
        for key, value in data.items():
            if field in value.get('endpoints', {}).values():
                return value.get('exemple', None)
        return None

    @staticmethod
    def get_field_for_endpoint(endpoint: NbaApiEndpoints, field: str):
        """Retourne le champ correspondant à un endpoint pour un champ donné."""
        data = NbaApiColumnMapper._load_json()

        # Vérifier que l'endpoint est valide
        if not endpoint:
            raise ValueError("L'argument 'endpoint' ne peut pas être None ou vide.")

        # Chercher dans les 'endpoints' pour le champ donné
        for key, value in data.items():
            endpoints = value.get('endpoints', {})
            for endpoint_key, endpoint_value in endpoints.items():
                if endpoint_value == field and endpoint_key == endpoint:
                    return key  # Retourner la clé du champ, ici 'player_id'
        return None

    @staticmethod
    def rename_columns(df: pd.DataFrame, endpoint: NbaApiEndpoints):
        """Renomme les colonnes d'un DataFrame selon les correspondances dans le fichier JSON en fonction de l'endpoint."""
        # Vérifier que l'endpoint est valide
        if not endpoint:
            raise ValueError("L'argument 'endpoint' ne peut pas être None ou vide.")

        # Crée un dictionnaire pour les nouvelles colonnes
        rename_dict = {}

        # Parcours chaque colonne du DataFrame
        for column in df.columns:
            # Récupère la référence pour la colonne
            reference = NbaApiColumnMapper.get_reference(column)

            # Essayer de récupérer le champ correspondant à l'endpoint
            field_for_endpoint = NbaApiColumnMapper.get_field_for_endpoint(endpoint, column)
            if field_for_endpoint:
                rename_dict[column] = field_for_endpoint
            elif reference:
                # Si la colonne a une référence, on la renomme avec cette référence
                rename_dict[column] = reference
            else:
                # Si la colonne n'est pas dans le fichier JSON, on la garde telle quelle
                rename_dict[column] = column
                print(f"Colonne {column} non renommée")

        # Renommer les colonnes du DataFrame
        return df.rename(columns=rename_dict)


if __name__ == "__main__":
    # Exemple d'utilisation pour renommer les colonnes
    df_avant = PlayerService.get_common_player_info_df_by_player_id(2544)
    df_apres = NbaApiColumnMapper.rename_columns(df_avant, NbaApiEndpoints.BOX_SCORE_TRADITIONAL_V3.value)
    print("toto")

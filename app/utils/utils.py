from datetime import datetime, date
from typing import Any

import pandas as pd
from pandas import DataFrame


class Utils:

    @staticmethod
    def obtenir_df_manipulable(data: Any, df_index: int = 0) -> DataFrame:

        # Vérifier si 'data' est un DataFrame
        if not isinstance(data, pd.DataFrame):
            df = data.get_data_frames()[df_index]  # Obtenir le DataFrame uniquement si data n'est pas déjà un DataFrame
        else:
            df = data

        df = df.astype(
            object)  # Convertir les types NumPy en types natifs Python, évite psycopg2: can't adapt type 'numpy.int64', cannot convert float NaN to integer
        df = Utils.convert_empty_to_none(df)
        df = Utils.convert_y_n_to_boolean(df)
        return df

    @staticmethod
    def ameliore_df(df: DataFrame) -> DataFrame:
        df = df.astype(
            object)  # Convertir les types NumPy en types natifs Python, évite psycopg2: can't adapt type 'numpy.int64', cannot convert float NaN to integer
        df = Utils.convert_empty_to_none(df)
        df = Utils.convert_y_n_to_boolean(df)
        return df

    @staticmethod
    def convert_to_date(date_str: str) -> date:
        """
        Convertit une date sous forme de chaîne en un objet datetime.date.
        Gère les formats :
        - 'APR 14, 2024'
        - '2025-01-30T00:00:00'

        :param date_str: La date sous forme de chaîne.
        :return: Un objet datetime.date correspondant.
        """
        try:
            return datetime.strptime(date_str, "%b %d, %Y").date()
        except ValueError:
            try:
                return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S").date()
            except ValueError:
                raise ValueError(f"Format de date inconnu : {date_str}")

    @staticmethod
    def convert_y_n_to_boolean(df: DataFrame) -> DataFrame:
        """
        Parcourt chaque élément d'un DataFrame et convertit les valeurs 'Y' en True
        et 'N' en False dans toutes les colonnes qui contiennent ces valeurs.
        """
        return df.map(lambda x: True if isinstance(x, str) and x.upper() == 'Y' else (
            False if isinstance(x, str) and x.upper() == 'N' else x))

    @staticmethod
    def convert_empty_to_none(df: DataFrame) -> DataFrame:
        """
        Remplace toutes les valeurs vides (chaînes vides, `None`, ou `NaN`) par `None` dans un DataFrame.
        Cette méthode garantit que les valeurs manquantes sont uniformément représentées par `None`,
        ce qui est l'équivalent de `NULL` en base de données.

        Elle utilise la méthode `map` de Pandas pour appliquer une transformation à chaque élément du DataFrame,
        remplaçant les valeurs vides par `None`.

        :param df: Le DataFrame sur lequel effectuer la conversion.
        :return: Un DataFrame où toutes les valeurs vides sont remplacées par `None`.
        """
        return df.map(lambda x: None if x in ("", None, float("nan")) else x)


if __name__ == "__main__":
    date_string = "APR 14, 2024"
    converted_date = Utils.convert_to_date(date_string)
    print(converted_date)  # Résultat : 2024-04-14

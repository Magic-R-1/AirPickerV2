from datetime import datetime, date


class Utils:

    @staticmethod
    def obtenir_df_manipulable(data):
        df = data.get_data_frames()[0]  # Obtenir le DataFrame
        df = Utils.convert_empty_to_none(df)
        df = df.astype(object) # Convertir les types NumPy en types natifs Python, évite psycopg2: can't adapt type 'numpy.int64', cannot convert float NaN to integer
        return df

    @staticmethod
    def convert_to_date(date_str: str) -> date:
        """
        Convertit une date sous forme de chaîne (format : 'APR 14, 2024') en un objet datetime.date.

        :param date_str: La date sous forme de chaîne.
        :return: Un objet datetime.date correspondant.
        """
        return datetime.strptime(date_str, "%b %d, %Y").date()


    @staticmethod
    def convert_yes_no_to_boolean(df):
        """
        Parcourt chaque élément d'un DataFrame et convertit les valeurs 'Y' en True
        et 'N' en False dans toutes les colonnes qui contiennent ces valeurs.
        """
        return df.map(lambda x: True if isinstance(x, str) and x.upper() == 'Y' else (False if isinstance(x, str) and x.upper() == 'N' else x))

    @staticmethod
    def convert_empty_to_none(df):
        """
        Cette méthode prend un DataFrame et remplace toutes les valeurs vides (comme des chaînes vides,
        des valeurs None, ou NaN) par `None` (qui est l'équivalent Python de `null` en base de données).

        :param df: Le DataFrame sur lequel effectuer la conversion.
        :return: Un DataFrame où toutes les valeurs vides sont remplacées par `None`.

        Cette méthode utilise la fonction `map` de Pandas pour itérer sur chaque élément du DataFrame
        et applique une condition qui vérifie si l'élément est une valeur vide (une chaîne vide,
        `None` ou NaN). Si c'est le cas, il est remplacé par `None`, sinon l'élément reste inchangé.
        """
        return df.map(lambda x: None if x in ("", None, float("nan")) else x)

if __name__ == "__main__":

    date_string = "APR 14, 2024"
    converted_date = Utils.convert_to_date(date_string)
    print(converted_date)  # Résultat : 2024-04-14

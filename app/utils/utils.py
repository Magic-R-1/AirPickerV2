class Utils:

    """
    Parcourt chaque élément d'un DataFrame et convertit les valeurs 'Y' en True
    et 'N' en False dans toutes les colonnes qui contiennent ces valeurs.
    """
    @staticmethod
    def convert_yes_no_to_boolean(df):
        return df.map(lambda x: True if isinstance(x, str) and x.upper() == 'Y' else (False if isinstance(x, str) and x.upper() == 'N' else x))
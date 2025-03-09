from marshmallow import ValidationError
from pandas import DataFrame

from app.models.boxscore import Boxscore
from app.schemas.boxscore_schema import BoxscoreSchema


class BoxscoreService:

    def __init__(self):
        pass

    @staticmethod
    def map_boxscore_df_to_list_boxscore_model(df_boxscore: DataFrame) -> list[Boxscore: dict]:
        """
        Convertit les données de l'API NBA en Boxscore en utilisant BoxscoreSchema.

        :param df_boxscore: DataFrame contenant les données boxscore.
        :return: Liste de dictionnaires représentant les objets Boxscore.
        """
        boxscore_dict = df_boxscore.to_dict(orient='records')  # Convertir le DataFrame en liste de dicts
        list_boxscore = []

        for boxscore_row in boxscore_dict:
            try:
                boxscore_schema = BoxscoreSchema().load(boxscore_row)
                boxscore_model = Boxscore(**boxscore_schema)
                list_boxscore.append(boxscore_model)

            except ValidationError as err:
                print(f"Erreur de validation sur la ligne {boxscore_row}: {err.messages}")

        return list_boxscore


if __name__ == "__main__":
    print("")

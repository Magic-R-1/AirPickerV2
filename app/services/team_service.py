from app.dao.team_dao import TeamDAO
from app.exceptions.exceptions import TeamNotFoundError
from app.schemas.team_schema import TeamSchema
from app.dto.team_dto import TeamDTO
from app.models.team import Team


class TeamService:

    def __init__(self):
        pass

    @staticmethod
    def get_team_dto_by_nickname(nickname: str):

        try:
            team_sql = TeamDAO.get_team_by_nickname(nickname)
        except (TeamNotFoundError, ValueError) as e:
            print(f"Erreur: {e}")
            return None

        team_dto = TeamDAO.team_from_sql_to_dto(team_sql)

        return team_dto

    @staticmethod
    def get_list_all_team_ids():
        list_from_db = TeamDAO.get_all_team_ids()
        return [team_id[0] for team_id in list_from_db]

    @staticmethod
    def map_static_team_to_team_model(team_data):
        """
        Mappe les données d'une équipe statique vers un objet TeamDTO en utilisant TeamSchema.

        :param team_data: Un tuple contenant une clé et les données d'équipe statique.
        :return: Une instance de TeamDTO ou None en cas d'erreur.
        """
        try:
            team_dict = team_data[1]  # Extraire les données de l'équipe

            # Vérifier et renommer la clé 'id' en 'team_id'
            team_dict['team_id'] = team_dict.pop('id')

            # Désérialisation des données pour obtenir un objet TeamDTO
            team_schema = TeamSchema().load(team_dict)

            # Création de Team à partir des données validées
            return Team(**team_schema)

        except Exception as e:
            print(f"Erreur lors du mapping des données de l'équipe : {e}")
            return None

    @staticmethod
    def map_static_team_to_team_dto(team_data):
        """
        Mappe les données d'une équipe statique vers un objet TeamDTO en utilisant TeamSchema.

        :param team_data: Un tuple contenant une clé et les données d'équipe statique.
        :return: Une instance de TeamDTO ou None en cas d'erreur.
        """
        try:
            team_dict = team_data[1]  # Extraire les données de l'équipe

            # Vérifier et renommer la clé 'id' en 'team_id'
            team_dict['team_id'] = team_dict.pop('id')

            # Désérialisation des données pour obtenir un objet TeamDTO
            team_schema = TeamSchema().load(team_dict)

            # Création de TeamDTO à partir des données validées
            return TeamDTO(**team_schema)

        except Exception as e:
            print(f"Erreur lors du mapping des données de l'équipe : {e}")
            return None


if __name__ == "__main__":
    all_team_ids = TeamService.get_list_all_team_ids()
    print("toto")

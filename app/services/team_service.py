from app.dao.team_dao import TeamDAO
from app.exceptions.exceptions import TeamNotFoundError
from app.schemas.team_schema import TeamSchema
from app.dto.team_dto import TeamDTO
from app.models.team import Team
from app.enums.nba_api_endpoints import NbaApiEndpoints
from app.utils.nba_api_column_mapper import NbaApiColumnMapper


class TeamService:

    def __init__(self):
        pass

    @staticmethod
    def get_team_dto_by_team_name(team_name: str):

        try:
            team_sql = TeamDAO.get_team_by_nickname(team_name)
        except (TeamNotFoundError, ValueError) as e:
            print(f"Erreur: {e}")
            return None

        team_dto = TeamDAO.team_from_sql_to_dto(team_sql)

        return team_dto

    @staticmethod
    def get_list_all_team_ids():
        list_from_db = TeamDAO.get_all_team_ids() # Récupère la liste des résultats de la BDD sous forme de tuple
        return [team_id[0] for team_id in list_from_db] # Extraction du premier élément de chaque tuple

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
            # Renommer les clés du dictionnaire
            # TODO : si méthode utilisée, remplacer par le rename columns, bien plus efficace
            team_dict_renamed = NbaApiColumnMapper.rename_keys_in_dict(team_data,NbaApiEndpoints.TEAMS_GET_TEAMS.value)

            # Désérialisation des données pour obtenir un objet TeamDTO
            team_schema = TeamSchema().load(team_dict_renamed)

            # Création de TeamDTO à partir des données validées
            return TeamDTO(**team_schema)

        except Exception as e:
            print(f"Erreur lors du mapping des données de l'équipe : {e}")
            return None

    @staticmethod
    def map_team_tuple_to_team_dto(team_tuple):
        """
        Convertit les données de l'API NBA en TeamDTO en utilisant TeamSchema.

        :param team_tuple: Tuple contenant les données de l'API NBA.
        :return: Instance de TeamDTO.
        """
        try:
            # Convertir le tuple en dictionnaire
            team_dict = team_tuple._asdict() # méthode couramment utilisée, ne pas tenir compte du warning

            # Utilisation de TeamSchema pour valider et structurer les données
            team_schema = TeamSchema().load(team_dict)  # Valide et prépare les données

            # Création de TeamDTO à partir des données validées
            return TeamDTO(**team_schema)

        except Exception as e:
            print(f"Erreur lors du mapping des données de l'équipe : {e}")
            return None


if __name__ == "__main__":
    all_team_ids = TeamService.get_list_all_team_ids()
    print("toto")

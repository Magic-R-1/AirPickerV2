from app.dto.player_dto import PlayerDTO
from app.dao.player_dao import PlayerDAO
from app.exceptions.exceptions import PlayerNotFoundError
from app.schemas.player_schema import PlayerSchema
from app.services.nba_api_service import NbaApiService
from app.utils.utils import Utils

class PlayerService:

    def __init__(self):
        pass

    @staticmethod
    def get_player_id_by_display_first_last(player_name: str):
        # TODO : à scinder
        # SQL
        try:
            player_sql = PlayerDAO.get_player_by_display_first_last(player_name)
        except (PlayerNotFoundError, ValueError) as e:
            print(f"Erreur: {e}")
            return None

        # Schema
        # Créer une instance du schéma pour sérialiser les données
        instance_player_schema = PlayerSchema()
        # Sérialiser l'objet SQLAlchemy en dictionnaire
        player_schema = instance_player_schema.dump(player_sql)

        # DTO
        player_dto = PlayerDTO(**player_schema)

        return player_dto.person_id

    @staticmethod
    def map_common_player_info_to_player_dto(player_data):
        # Mapping complet des données vers le DTO
        return PlayerDTO(
            person_id = player_data['PERSON_ID'].iloc[0],
            first_name = player_data['FIRST_NAME'].iloc[0],
            last_name = player_data['LAST_NAME'].iloc[0],
            display_first_last = player_data['DISPLAY_FIRST_LAST'].iloc[0],
            display_last_comma_first = player_data['DISPLAY_LAST_COMMA_FIRST'].iloc[0],
            display_fi_last = player_data['DISPLAY_FI_LAST'].iloc[0],
            player_slug = player_data['PLAYER_SLUG'].iloc[0],
            birthdate = player_data['BIRTHDATE'].iloc[0],
            school = player_data['SCHOOL'].iloc[0],
            country = player_data['COUNTRY'].iloc[0],
            last_affiliation = player_data['LAST_AFFILIATION'].iloc[0],
            height = player_data['HEIGHT'].iloc[0],
            weight = player_data['WEIGHT'].iloc[0],
            season_exp = player_data['SEASON_EXP'].iloc[0],
            jersey = player_data['JERSEY'].iloc[0],
            position = player_data['POSITION'].iloc[0],
            roster_status = player_data['ROSTERSTATUS'].iloc[0],
            team_id = player_data['TEAM_ID'].iloc[0],
            team_name = player_data['TEAM_NAME'].iloc[0],
            team_abbreviation = player_data['TEAM_ABBREVIATION'].iloc[0],
            team_code = player_data['TEAM_CODE'].iloc[0],
            team_city = player_data['TEAM_CITY'].iloc[0],
            player_code = player_data['PLAYERCODE'].iloc[0],
            from_year = player_data['FROM_YEAR'].iloc[0],
            to_year = player_data['TO_YEAR'].iloc[0],
            dleague_flag = player_data['DLEAGUE_FLAG'].iloc[0],
            nba_flag = player_data['NBA_FLAG'].iloc[0],
            games_played_flag = player_data['GAMES_PLAYED_FLAG'].iloc[0],
            draft_year = player_data['DRAFT_YEAR'].iloc[0],
            draft_round = player_data['DRAFT_ROUND'].iloc[0],
            draft_number = player_data['DRAFT_NUMBER'].iloc[0]
        )

    @staticmethod
    def person_id_to_common_player_info_df(person_id: int):
        player_info = NbaApiService.common_player_info(person_id)
        player_data = player_info.get_data_frames()[0]              # Obtenir le DataFrame
        player_data = Utils.convert_yes_no_to_boolean(player_data)
        player_data = Utils.convert_empty_to_none(player_data)
        player_data = player_data.astype(object)                    # Convertir les types NumPy en types natifs Python, évite psycopg2: can't adapt type 'numpy.int64'

        return player_data

    @staticmethod
    def get_active_players():
        list_players = NbaApiService.get_players()

        # Compréhension de liste pour filtrer les joueurs actifs
        list_active_players = [player for player in list_players if player['is_active']]

        return list_active_players

if __name__ == "__main__":

    player_id = PlayerService.get_player_id_by_display_first_last("LeBron James")
    print(player_id)
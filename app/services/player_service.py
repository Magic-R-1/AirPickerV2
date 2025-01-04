from app.dto.player_dto import PlayerDTO
from app.services.nba_api_service import NbaApiService

class PlayerService:

    def __init__(self):
        pass

    @staticmethod
    def get_player_id_by_name(player_name):

        player_list = NbaApiService.get_players() # TODO : appel API, à optimiser

        # Recherche du joueur par son nom
        player = next((player for player in player_list if player['full_name'] == player_name), None)

        if player:
            return player['id']
        else:
            raise ValueError(f"Le joueur '{player_name}' n'a pas été trouvé.")

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
from app.dto.team_dto import TeamDTO
from app.services.nba_api_service import NbaApiService


class TeamService:

    def __init__(self):
        pass

    @staticmethod
    def get_teams():
        return NbaApiService.get_teams()

    @staticmethod
    def map_static_team_to_team_dto(team_data):
        # Mapping complet des données vers le DTO
        return TeamDTO(
            team_id = team_data[1]['id'],
            full_name = team_data[1]['full_name'],
            abbreviation = team_data[1]['abbreviation'],
            nickname = team_data[1]['nickname'],
            city = team_data[1]['city'],
            state = team_data[1]['state'],
            year_founded = team_data[1]['year_founded']
        )


import pandas as pd

from app.services.nba_api_service import NbaApiService


class CommonTeamRosterService:

    def __init__(self):
        pass

    @staticmethod
    def get_team_roster_by_team_id(team_id: int) -> pd.DataFrame | None :
        """
        Utile la méthode de NbaApiService pour obtenir le DF de CommonTeamRoster

        :param team_id: L'identifiant unique du match.
        :return: Un DataFrame contenant les données du commonteamroster ou None en cas d'erreur.
        """
        try:
            return NbaApiService.get_team_roster_by_team_id(team_id)

        except Exception as e:
            print(f"Erreur lors de la récupération des données pour le commonteamroster {team_id}: {e}")
            return None


if __name__ == "__main__":
    df_boxscore = CommonTeamRosterService.get_team_roster_by_team_id(1610612747)
    print("")
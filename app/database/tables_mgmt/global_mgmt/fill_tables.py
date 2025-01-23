from app.database.tables_mgmt.unit_mgmt.team_table_mgmt import TeamTableLifeCycle
from app.database.tables_mgmt.unit_mgmt.player_table_mgmt import PlayerTableLifeCycle


class FillTables:

    @staticmethod
    def fill_all_tables():
        TeamTableLifeCycle.fill_team_table()
        PlayerTableLifeCycle.fill_player_table()

if __name__ == "__main__":
    FillTables.fill_all_tables()
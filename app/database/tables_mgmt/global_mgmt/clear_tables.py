from app.database.tables_mgmt.unit_mgmt.team_table_mgmt import TeamTableLifeCycle
from app.database.tables_mgmt.unit_mgmt.player_table_mgmt import PlayerTableLifeCycle


class ClearTables:

    @staticmethod
    def clear_all_tables():
        TeamTableLifeCycle.clear_team_table()
        PlayerTableLifeCycle.clear_player_table()

if __name__ == "__main__":
    ClearTables.clear_all_tables()
from app.database.tables_mgmt.unit_mgmt.team_table_mgmt import TeamTableMgmt
from app.database.tables_mgmt.unit_mgmt.player_table_mgmt import PlayerTableMgmt


class ClearTables:

    @staticmethod
    def clear_all_tables():
        TeamTableMgmt.clear_team_table()
        PlayerTableMgmt.clear_player_table()

if __name__ == "__main__":
    ClearTables.clear_all_tables()
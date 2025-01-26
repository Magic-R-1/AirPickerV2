from app.database.tables_mgmt.unit_mgmt.team_table_mgmt import TeamTableMgmt
from app.database.tables_mgmt.unit_mgmt.player_table_mgmt import PlayerTableMgmt
from app.database.tables_mgmt.unit_mgmt.boxscore_table_mgmt import BoxscoreTableMgmt
from app.database.tables_mgmt.unit_mgmt.teamgamelog_table_mgmt import TeamGameLogTableMgmt


class ClearTables:

    @staticmethod
    def clear_all_tables():
        BoxscoreTableMgmt.clear_boxscore_table()
        TeamGameLogTableMgmt.clear_teamgamelog_table()
        PlayerTableMgmt.clear_player_table()
        TeamTableMgmt.clear_team_table()

if __name__ == "__main__":
    ClearTables.clear_all_tables()
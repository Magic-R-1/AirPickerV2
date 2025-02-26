from app.database.tables_mgmt.unit_mgmt.boxscore_table_mgmt import BoxscoreTableMgmt
from app.database.tables_mgmt.unit_mgmt.player_table_mgmt import PlayerTableMgmt
from app.database.tables_mgmt.unit_mgmt.team_table_mgmt import TeamTableMgmt
from app.database.tables_mgmt.unit_mgmt.teamgamelog_table_mgmt import TeamGameLogTableMgmt


class DropTables:

    @staticmethod
    def drop_all_tables():
        BoxscoreTableMgmt.drop_boxscore_table()
        # TeamGameLogTableMgmt.drop_teamgamelog_table()
        PlayerTableMgmt.drop_player_table()
        TeamTableMgmt.drop_team_table()
        
if __name__ == "__main__":
    DropTables.drop_all_tables()
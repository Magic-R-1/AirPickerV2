from app.database.tables_mgmt.unit_mgmt.boxscore_table_mgmt import BoxscoreTableMgmt
from app.database.tables_mgmt.unit_mgmt.player_table_mgmt import PlayerTableMgmt
from app.database.tables_mgmt.unit_mgmt.team_table_mgmt import TeamTableMgmt
from app.database.tables_mgmt.unit_mgmt.teamgamelog_table_mgmt import TeamGameLogTableMgmt


class DropTables:

    @staticmethod
    def drop_all_tables():
        PlayerTableMgmt.drop_player_table()
        TeamTableMgmt.drop_team_table()
        #BoxscoreTableLifeCycle.drop_boxscore_table()
        #TeamGameLogTableLifeCycle.drop_teamgamelog_table()

if __name__ == "__main__":
    DropTables.drop_all_tables()
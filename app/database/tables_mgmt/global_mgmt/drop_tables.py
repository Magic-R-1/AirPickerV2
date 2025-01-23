from app.database.tables_mgmt.unit_mgmt.boxscore_table_mgmt import BoxscoreTableLifeCycle
from app.database.tables_mgmt.unit_mgmt.player_table_mgmt import PlayerTableLifeCycle
from app.database.tables_mgmt.unit_mgmt.team_table_mgmt import TeamTableLifeCycle
from app.database.tables_mgmt.unit_mgmt.teamgamelog_table_mgmt import TeamGameLogTableLifeCycle


class DropTables:

    @staticmethod
    def drop_all_tables():
        PlayerTableLifeCycle.drop_player_table()
        TeamTableLifeCycle.drop_team_table()
        #BoxscoreTableLifeCycle.drop_boxscore_table()
        #TeamGameLogTableLifeCycle.drop_teamgamelog_table()

if __name__ == "__main__":
    DropTables.drop_all_tables()
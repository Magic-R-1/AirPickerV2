from app.database.tables_mgmt.unit_mgmt.team_table_mgmt import TeamTableMgmt
from app.database.tables_mgmt.unit_mgmt.player_table_mgmt import PlayerTableMgmt
from app.database.tables_mgmt.unit_mgmt.boxscore_table_mgmt import BoxscoreTableMgmt
from app.database.tables_mgmt.unit_mgmt.teamgamelog_table_mgmt import TeamGameLogTableMgmt
from app.database.db_connector import engine, Base

class CreateTables:

    @staticmethod
    def create_all_tables():
        # Base.metadata.create_all(engine)
        # TeamTableLifeCycle.create_team_table()
        # PlayerTableLifeCycle.create_player_table()
        # BoxscoreTableLifeCycle.create_boxscore_table()
        TeamGameLogTableMgmt.create_teamgamelog_table()

if __name__ == "__main__":
    CreateTables.create_all_tables()
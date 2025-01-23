from app.database.tables_mgmt.unit_mgmt.team_table_mgmt import TeamTableLifeCycle
from app.database.tables_mgmt.unit_mgmt.player_table_mgmt import PlayerTableLifeCycle
from app.database.tables_mgmt.unit_mgmt.boxscore_table_mgmt import BoxscoreTableLifeCycle
from app.database.tables_mgmt.unit_mgmt.teamgamelog_table_mgmt import TeamGameLogTableLifeCycle
from app.database.db_connector import engine
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class CreateTables:

    @staticmethod
    def create_all_tables():
        # Base.metadata.create_all(engine)
        # TeamTableLifeCycle.create_team_table()
        # PlayerTableLifeCycle.create_player_table()
        # BoxscoreTableLifeCycle.create_boxscore_table()
        TeamGameLogTableLifeCycle.create_teamgamelog_table()

if __name__ == "__main__":
    CreateTables.create_all_tables()
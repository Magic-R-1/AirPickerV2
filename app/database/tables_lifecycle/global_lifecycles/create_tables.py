from app.database.tables_lifecycle.tables_lifecycles.player_table_lifecycle import PlayerTableLifeCycle
from app.database.tables_lifecycle.tables_lifecycles.team_table_lifecycle import TeamTableLifeCycle


class CreateTables:

    @staticmethod
    def create_all_tables():
        # Base.metadata.create_all(engine)
        TeamTableLifeCycle.create_team_table()
        PlayerTableLifeCycle.create_player_table()

if __name__ == "__main__":
    CreateTables.create_all_tables()
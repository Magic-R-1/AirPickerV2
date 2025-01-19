from app.database.tables_lifecycle.tables_lifecycles.player_table_lifecycle import PlayerTableLifeCycle
from app.database.tables_lifecycle.tables_lifecycles.team_table_lifecycle import TeamTableLifeCycle


class DropTables:

    @staticmethod
    def drop_all_tables():
        TeamTableLifeCycle.drop_team_table()
        PlayerTableLifeCycle.drop_player_table()

if __name__ == "__main__":
    DropTables.drop_all_tables()
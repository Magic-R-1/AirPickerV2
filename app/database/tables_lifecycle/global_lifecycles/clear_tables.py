from app.database.tables_lifecycle.tables_lifecycles.team_table_lifecycle import TeamTableLifeCycle
from app.database.tables_lifecycle.tables_lifecycles.player_table_lifecycle import PlayerTableLifeCycle


class ClearTables:

    @staticmethod
    def clear_all_tables():
        TeamTableLifeCycle.clear_team_table()
        PlayerTableLifeCycle.clear_player_table()

if __name__ == "__main__":
    ClearTables.clear_all_tables()
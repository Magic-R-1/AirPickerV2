from app.database.tables_lifecycle.tables_lifecycles.team_table_lifecycle import TeamTableLifeCycle
from app.database.tables_lifecycle.tables_lifecycles.player_table_lifecycle import PlayerTableLifeCycle


class FillTables:

    @staticmethod
    def fill_all_tables():
        TeamTableLifeCycle.fill_team_table()
        PlayerTableLifeCycle.fill_player_table()

if __name__ == "__main__":
    FillTables.fill_all_tables()
from app.database.tables_mgmt.unit_mgmt.team_table_mgmt import TeamTableMgmt
from app.database.tables_mgmt.unit_mgmt.player_table_mgmt import PlayerTableMgmt


class FillTables:

    @staticmethod
    def fill_all_tables():
        TeamTableMgmt.fill_team_table()
        PlayerTableMgmt.fill_player_table()

if __name__ == "__main__":
    FillTables.fill_all_tables()
from app.database.tables_mgmt.unit_mgmt.teamgamelog_table_mgmt import TeamGameLogTableMgmt


class DatabaseDailyUpdate:

    @staticmethod
    def database_daily_update():
        TeamGameLogTableMgmt.update_teamgamelog_table()

if __name__ == "__main__":
    DatabaseDailyUpdate.database_daily_update()
from app.database.tables_lifecycle.player_table_lifecycle.team_table_lifecycle import TeamTableLifeCycle
from app.database.tables_lifecycle.player_table_lifecycle.player_table_lifecycle import PlayerTableLifeCycle


class ClearTables:
    TeamTableLifeCycle.clear_team_table()
    PlayerTableLifeCycle.clear_player_table()
from app.database.tables_lifecycle.player_table_lifecycle.team_table_lifecycle import TeamTableLifeCycle
from app.database.tables_lifecycle.player_table_lifecycle.player_table_lifecycle import PlayerTableLifeCycle


class FillTables:
    TeamTableLifeCycle.fill_team_table()
    PlayerTableLifeCycle.fill_player_table()

from app.dao.player_dao import PlayerDAO


class ClearTables:
    PlayerDAO.clear_player_table()
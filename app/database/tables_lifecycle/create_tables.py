from app.dao.player_dao import PlayerDAO


class CreateTables:
    PlayerDAO.create_player_table()
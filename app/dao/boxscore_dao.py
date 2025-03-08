from typing import List

from app.database.db_connector import session_scope
from app.models import Boxscore


class BoxscoreDAO:

    # 1. CRUD
    # =================================

    @staticmethod
    def get_list_unique_game_ids() -> List[str]:
        """
        Récupère la liste des game_id uniques depuis la table teamgamelog.

        :return: Liste des game_id uniques.
        """
        with session_scope() as session:
            unique_game_ids = session.query(Boxscore.game_id).distinct().all()
            return [row[0] for row in unique_game_ids]
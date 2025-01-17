from app.database.declarative_base import Base
from app.database.db_connector import engine
from app.models import Player, Team

class CreateTables:

    @staticmethod
    def create_all_tables():
        Base.metadata.create_all(engine)

if __name__ == "__main__":
    CreateTables.create_all_tables()
from app.database.db_connector import engine
from app.dto.player_dto import PlayerDTO

def create_table_player():

    # Base.metadata.create_all(engine) # Pour créer toutes les classes héritant de Base
    PlayerDTO.__table__.create(engine)

    print("Table 'player' créée avec succès.")

if __name__ == "__main__":
    create_table_player()
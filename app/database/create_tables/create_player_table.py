from app.database.db_connector import engine
from app.models.player import Player

def create_table_player():

    # Base.metadata.create_all(engine) # Pour créer toutes les classes héritant de Base
    Player.__table__.create(engine)

    print("Table 'player' créée avec succès.")

if __name__ == "__main__":
    create_table_player()
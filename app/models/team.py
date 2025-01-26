from sqlalchemy import Column, Integer, String
from app.database.db_connector import Base


class Team(Base):

    # Nom de la table dans la base de données
    __tablename__ = 'team'

    # Nom des colonnes dans la base de données
    team_id = Column(Integer, primary_key=True)

    team_full_name = Column(String, nullable=True)
    team_tricode = Column(String, nullable=True)
    team_name = Column(String, nullable=True)

    team_city = Column(String, nullable=True)
    team_state = Column(String, nullable=True)

    year_founded = Column(Integer, nullable=True)

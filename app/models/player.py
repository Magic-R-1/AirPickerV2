from sqlalchemy import Column, Integer, String, Float, Boolean, Date
from sqlalchemy.ext.declarative import declarative_base
 
# Définir la base pour SQLAlchemy
Base = declarative_base()

class Player(Base):
    __tablename__ = 'player'  # Nom de la table dans la base de données

    # Définition des colonnes
    person_id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    display_first_last = Column(String, nullable=True)
    display_last_comma_first = Column(String, nullable=True)
    display_fi_last = Column(String, nullable=True)
    player_slug = Column(String, nullable=True)
    birthdate = Column(Date, nullable=True)
    school = Column(String, nullable=True)
    country = Column(String, nullable=True)
    last_affiliation = Column(String, nullable=True)
    height = Column(String, nullable=True)
    weight = Column(Float, nullable=True)
    season_exp = Column(Integer, nullable=True)
    jersey = Column(Integer, nullable=True)
    position = Column(String, nullable=True)
    roster_status = Column(String, nullable=True)
    team_id = Column(Integer, nullable=True)
    team_name = Column(String, nullable=True)
    team_abbreviation = Column(String, nullable=True)
    team_code = Column(String, nullable=True)
    team_city = Column(String, nullable=True)
    player_code = Column(String, nullable=True)
    from_year = Column(Integer, nullable=True)
    to_year = Column(Integer, nullable=True)
    dleague_flag = Column(Boolean, nullable=True)
    nba_flag = Column(Boolean, nullable=True)
    games_played_flag = Column(Boolean, nullable=True)
    draft_year = Column(String, nullable=True)
    draft_round = Column(String, nullable=True)
    draft_number = Column(String, nullable=True)

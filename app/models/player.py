from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database.db_connector import Base
from app.models.team import Team # À conserver, pour la relation


class Player(Base):

    # Nom de la table dans la base de données
    __tablename__ = 'player'

    # Nom des colonnes dans la base de données
    player_id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=True)
    family_name = Column(String, nullable=True)
    display_first_last = Column(String, nullable=True)
    display_last_comma_first = Column(String, nullable=True)
    display_fi_last = Column(String, nullable=True)
    player_slug = Column(String, nullable=True)

    birthdate = Column(Date, nullable=True)
    school = Column(String, nullable=True)
    country = Column(String, nullable=True)
    last_affiliation = Column(String, nullable=True)
    height = Column(String, nullable=True)
    weight = Column(Integer, nullable=True)
    season_exp = Column(Integer, nullable=True)
    jersey_num = Column(Integer, nullable=True)
    full_position = Column(String, nullable=True)
    roster_status = Column(String, nullable=True)

    team_id = Column(Integer, ForeignKey("team.team_id"), nullable=True)
    team_name = Column(String, nullable=True)
    team_tricode = Column(String, nullable=True)
    team_slug = Column(String, nullable=True)
    team_city = Column(String, nullable=True)

    player_code = Column(String, nullable=True)
    from_year = Column(Integer, nullable=True)
    to_year = Column(Integer, nullable=True)

    dleague_flag = Column(Boolean, nullable=True)
    nba_flag = Column(Boolean, nullable=True)
    games_played_flag = Column(Boolean, nullable=True)
    games_played_current_season_flag  = Column(Boolean, nullable=True)
    greatest_75_flag = Column(Boolean, nullable=True)

    draft_year = Column(String, nullable=True)      # String car peut être Undrafted
    draft_round = Column(String, nullable=True)     # String car peut être Undrafted
    draft_number = Column(String, nullable=True)    # String car peut être Undrafted

    # Relations
    team = relationship("Team", backref=None, lazy='joined')
    # boxscores = relationship("Boxscore", backref=None, lazy='joined')

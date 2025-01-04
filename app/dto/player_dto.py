from sqlalchemy import Column, Integer, String, Float, Boolean, Date
from sqlalchemy.ext.declarative import declarative_base

# Définir la base pour SQLAlchemy
Base = declarative_base()

class PlayerDTO(Base):
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

    def __init__(self, person_id=None, first_name=None, last_name=None, display_first_last=None,
                 display_last_comma_first=None, display_fi_last=None, player_slug=None, birthdate=None,
                 school=None, country=None, last_affiliation=None, height=None, weight=None, season_exp=None,
                 jersey=None, position=None, roster_status=None, team_id=None, team_name=None,
                 team_abbreviation=None, team_code=None, team_city=None, player_code=None, from_year=None,
                 to_year=None, dleague_flag=None, nba_flag=None, games_played_flag=None, draft_year=None,
                 draft_round=None, draft_number=None):
        self.person_id = person_id
        self.first_name = first_name
        self.last_name = last_name
        self.display_first_last = display_first_last
        self.display_last_comma_first = display_last_comma_first
        self.display_fi_last = display_fi_last
        self.player_slug = player_slug
        self.birthdate = birthdate
        self.school = school
        self.country = country
        self.last_affiliation = last_affiliation
        self.height = height
        self.weight = weight
        self.season_exp = season_exp
        self.jersey = jersey
        self.position = position
        self.roster_status = roster_status
        self.team_id = team_id
        self.team_name = team_name
        self.team_abbreviation = team_abbreviation
        self.team_code = team_code
        self.team_city = team_city
        self.player_code = player_code
        self.from_year = from_year
        self.to_year = to_year
        self.dleague_flag = dleague_flag
        self.nba_flag = nba_flag
        self.games_played_flag = games_played_flag
        self.draft_year = draft_year
        self.draft_round = draft_round
        self.draft_number = draft_number

    def __repr__(self):
        # Permet d'afficher quelque chose de propre, en debug par exemple, plutôt que <dto.player_dto.PlayerDTO object at 0x1037b0c20>
        return f"PlayerDTO({self.person_id}, {self.first_name} {self.last_name}, {self.team_name})"

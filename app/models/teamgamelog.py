from sqlalchemy import Column, String, Integer, Float, Date, ForeignKey
from app.database.declarative_base import Base

class TeamGameLog(Base):
    # Nom de la table dans la base de données
    __tablename__ = 'teamgamelog'

    # TODO : passer tous les champs en minuscule au moment de l'appel API
    # Nom des colonnes dans la base de données
    team_id = Column(Integer, ForeignKey('team.team_id'), primary_key=True)     # Clé primaire composée, et clé étrangère
    game_id = Column(String, primary_key=True)  # Clé primaire composée. Pas de clé étrangère, car table teamgamelog mise à jour avant boxscore : IntegrityError
    game_date = Column(String, nullable=False)
    matchup = Column(String, nullable=False)
    wl = Column(String, nullable=True)
    w = Column(Integer, nullable=True)
    l = Column(Integer, nullable=True)
    w_pct = Column(Float, nullable=True)
    min = Column(Float, nullable=True)
    fgm = Column(Integer, nullable=True)
    fga = Column(Integer, nullable=True)
    fg_pct = Column(Float, nullable=True)
    fg3m = Column(Integer, nullable=True)
    fg3a = Column(Integer, nullable=True)
    fg3_pct = Column(Float, nullable=True)
    ftm = Column(Integer, nullable=True)
    fta = Column(Integer, nullable=True)
    ft_pct = Column(Float, nullable=True)
    oreb = Column(Integer, nullable=True)
    dreb = Column(Integer, nullable=True)
    reb = Column(Integer, nullable=True)
    ast = Column(Integer, nullable=True)
    stl = Column(Integer, nullable=True)
    blk = Column(Integer, nullable=True)
    tov = Column(Integer, nullable=True)
    pf = Column(Integer, nullable=True)
    pts = Column(Integer, nullable=True)

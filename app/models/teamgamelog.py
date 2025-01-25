from sqlalchemy import Column, String, Integer, Float, ForeignKey, Date
from app.database.declarative_base import Base


class TeamGameLog(Base):

    # Nom de la table dans la base de données
    __tablename__ = 'teamgamelog'

    # Nom des colonnes dans la base de données
    team_id = Column(Integer, ForeignKey('team.team_id'), primary_key=True) # Clé primaire composée, et clé étrangère

    game_id = Column(String, primary_key=True)  # Clé primaire composée. Pas de clé étrangère, car table teamgamelog mise à jour avant boxscore : IntegrityError
    # TODO : à convertir en Date, pour le moment : APR 14, 2024
    # Utils.convert_to_date(date_string)
    game_date = Column(Date, nullable=False)
    # game_date = Column(String, nullable=False)
    matchup = Column(String, nullable=False)

    wl = Column(String, nullable=True)
    w = Column(Integer, nullable=True)
    l = Column(Integer, nullable=True)
    w_pct = Column(Float, nullable=True)

    minutes = Column(Integer, nullable=True)

    fgm = Column(Integer, nullable=True)
    fga = Column(Integer, nullable=True)
    fg_pct = Column(Float, nullable=True)
    fg3m = Column(Integer, nullable=True)
    fg3a = Column(Integer, nullable=True)
    fg3_pct = Column(Float, nullable=True)
    ftm = Column(Integer, nullable=True)
    fta = Column(Integer, nullable=True)
    ft_pct = Column(Float, nullable=True)

    o_reb = Column(Integer, nullable=True)
    d_reb = Column(Integer, nullable=True)
    reb = Column(Integer, nullable=True)

    ast = Column(Integer, nullable=True)
    stl = Column(Integer, nullable=True)
    blk = Column(Integer, nullable=True)
    tov = Column(Integer, nullable=True)
    pf = Column(Integer, nullable=True)
    pts = Column(Integer, nullable=True)

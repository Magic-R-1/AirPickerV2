from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.database.db_connector import Base

class Boxscore(Base):
    # Nom de la table dans la base de données
    __tablename__ = 'boxscore'

    # Nom des colonnes dans la base de données
    game_id = Column(String, primary_key=True)  # Utilisation d'une clé primaire composée (game_id et person_id). String car les id commencent par 00

    team_id = Column(Integer, ForeignKey("team.team_id"), nullable=True)    # Clé étrangère vers la table Team
    team_city = Column(String, nullable=True)
    team_name = Column(String, nullable=True)
    team_tricode = Column(String, nullable=True)
    team_slug = Column(String, nullable=True)

    player_id = Column(Integer, ForeignKey('player.player_id'), primary_key=True)  # Utilisation de player_id dans la clé primaire, et clé étrangère vers la table Player
    first_name = Column(String, nullable=True)
    family_name = Column(String, nullable=True)
    display_fi_last = Column(String, nullable=True)
    player_slug = Column(String, nullable=True)
    position = Column(String, nullable=True)
    comment = Column(String, nullable=True)
    jersey_num = Column(Integer, nullable=True)
    minutes = Column(String, nullable=True)

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
    plus_minus_points = Column(Float, nullable=True)

    # Utilisation d'un index composite si nécessaire
    __table_args__ = (
        # Ajouter une contrainte unique pour éviter les doublons avec game_id + person_id
        {"sqlite_autoincrement": True},
    )

    def __repr__(self):
        return f"<Boxscore(game_id={self.game_id}, person_id={self.person_id}, points={self.points})>"

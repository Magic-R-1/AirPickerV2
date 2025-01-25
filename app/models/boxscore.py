from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.database.declarative_base import Base

class Boxscore(Base):
    # Nom de la table dans la base de données
    __tablename__ = 'boxscore'

    # Nom des colonnes dans la base de données
    game_id = Column(String, primary_key=True)  # Utilisation d'une clé primaire composée (game_id et person_id)
    team_id = Column(Integer, ForeignKey("team.team_id"), nullable=True)    # Clé étrangère vers la table Team
    team_city = Column(String, nullable=True)
    team_name = Column(String, nullable=True)
    team_tricode = Column(String, nullable=True)
    team_slug = Column(String, nullable=True)
    player_id = Column(Integer, ForeignKey('player.player_id'), primary_key=True)  # Utilisation de player_id dans la clé primaire, et clé étrangère vers la table Player
    first_name = Column(String, nullable=True)
    family_name = Column(String, nullable=True)
    name_i = Column(String, nullable=True)
    player_slug = Column(String, nullable=True)
    position = Column(String, nullable=True)
    comment = Column(String, nullable=True)
    jersey_num = Column(Integer, nullable=True)
    minutes = Column(Float, nullable=True)
    field_goals_made = Column(Integer, nullable=True)
    field_goals_attempted = Column(Integer, nullable=True)
    field_goals_percentage = Column(Float, nullable=True)
    three_pointers_made = Column(Integer, nullable=True)
    three_pointers_attempted = Column(Integer, nullable=True)
    three_pointers_percentage = Column(Float, nullable=True)
    free_throws_made = Column(Integer, nullable=True)
    free_throws_attempted = Column(Integer, nullable=True)
    free_throws_percentage = Column(Float, nullable=True)
    rebounds_offensive = Column(Integer, nullable=True)
    rebounds_defensive = Column(Integer, nullable=True)
    rebounds_total = Column(Integer, nullable=True)
    assists = Column(Integer, nullable=True)
    steals = Column(Integer, nullable=True)
    blocks = Column(Integer, nullable=True)
    turnovers = Column(Integer, nullable=True)
    fouls_personal = Column(Integer, nullable=True)
    points = Column(Integer, nullable=True)
    plus_minus_points = Column(Float, nullable=True)

    # Utilisation d'un index composite si nécessaire
    __table_args__ = (
        # Ajouter une contrainte unique pour éviter les doublons avec game_id + person_id
        {"sqlite_autoincrement": True},
    )

    def __repr__(self):
        return f"<Boxscore(game_id={self.game_id}, person_id={self.person_id}, points={self.points})>"

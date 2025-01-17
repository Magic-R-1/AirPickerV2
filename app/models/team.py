from sqlalchemy import Column, Integer, String, Float, Boolean, Date
from sqlalchemy.orm import relationship
from app.database.declarative_base import Base


class Team(Base):
    __tablename__ = 'team'  # Nom de la table dans la base de données

    # Définition des colonnes
    team_id = Column(Integer, primary_key=True)
    full_name = Column(String, nullable=True)
    abbreviation = Column(String, nullable=True)
    nickname = Column(String, nullable=True)
    city = Column(String, nullable=True)
    state = Column(String, nullable=True)
    year_founded = Column(Integer, nullable=True)

    # Relation avec Player
    players = relationship("Player", back_populates="team")  # Relation one-to-many

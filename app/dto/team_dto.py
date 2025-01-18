from dataclasses import dataclass, field
from typing import Optional


@dataclass
class TeamDTO:

    # Attributs provenant de la base de données
    team_id: [int] = None
    full_name: Optional[str] = None
    abbreviation: Optional[str] = None
    nickname: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    year_founded: Optional[int] = None

    # Attributs relationnels
    # players: Optional[List[PlayerDTO]] = None

    # Attributs fonctionnels
    #

    def __repr__(self):
        # Affichage propre pour le débogage ou la journalisation
        return f"TeamDTO(id={self.team_id}, full_name={self.full_name}, abbreviation={self.abbreviation}, city={self.city})"

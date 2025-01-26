from dataclasses import dataclass
from typing import Optional


@dataclass
class TeamDTO:

    # Attributs provenant de la base de données
    team_id: [int] = None

    team_full_name: Optional[str] = None
    team_tricode: Optional[str] = None
    team_name: Optional[str] = None

    team_city: Optional[str] = None
    team_state: Optional[str] = None

    year_founded: Optional[int] = None


    def __repr__(self):
        # Affichage propre pour le débogage ou la journalisation
        return f"TeamDTO(id={self.team_id}, {self.team_full_name})"

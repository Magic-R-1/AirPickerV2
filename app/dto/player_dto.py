from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class PlayerDTO:
    person_id: [int] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    display_first_last: Optional[str] = None
    display_last_comma_first: Optional[str] = None
    display_fi_last: Optional[str] = None
    player_slug: Optional[str] = None
    birthdate: Optional[date] = None
    school: Optional[str] = None
    country: Optional[str] = None
    last_affiliation: Optional[str] = None
    height: Optional[str] = None
    weight: Optional[float] = None
    season_exp: Optional[int] = None
    jersey: Optional[int] = None
    position: Optional[str] = None
    roster_status: Optional[str] = None
    team_id: Optional[int] = None
    team_name: Optional[str] = None
    team_abbreviation: Optional[str] = None
    team_code: Optional[str] = None
    team_city: Optional[str] = None
    player_code: Optional[str] = None
    from_year: Optional[int] = None
    to_year: Optional[int] = None
    dleague_flag: Optional[bool] = None
    nba_flag: Optional[bool] = None
    games_played_flag: Optional[bool] = None
    draft_year: Optional[str] = None
    draft_round: Optional[str] = None
    draft_number: Optional[str] = None

    def __repr__(self):
        # Permet d'afficher quelque chose de propre, en debug par exemple, plutôt que <dto.player_dto.PlayerDTO object at 0x1037b0c20>
        return f"PlayerDTO({self.person_id}, {self.first_name} {self.last_name}, {self.team_name})"

from dataclasses import dataclass
from typing import Optional


@dataclass
class BoxscoreDTO:

    # Attributs provenant de la base de données
    game_id: str
    team_id: Optional[int]
    team_city: Optional[str]
    team_name: Optional[str]
    team_tricode: Optional[str]
    team_slug: Optional[str]
    player_id: int
    first_name: Optional[str]
    family_name: Optional[str]
    name_i: Optional[str]
    player_slug: Optional[str]
    position: Optional[str]
    comment: Optional[str]
    jersey_num: Optional[int]
    minutes: Optional[float]
    field_goals_made: Optional[int]
    field_goals_attempted: Optional[int]
    field_goals_percentage: Optional[float]
    three_pointers_made: Optional[int]
    three_pointers_attempted: Optional[int]
    three_pointers_percentage: Optional[float]
    free_throws_made: Optional[int]
    free_throws_attempted: Optional[int]
    free_throws_percentage: Optional[float]
    rebounds_offensive: Optional[int]
    rebounds_defensive: Optional[int]
    rebounds_total: Optional[int]
    assists: Optional[int]
    steals: Optional[int]
    blocks: Optional[int]
    turnovers: Optional[int]
    fouls_personal: Optional[int]
    points: Optional[int]
    plus_minus_points: Optional[float]

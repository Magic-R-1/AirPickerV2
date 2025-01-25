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
    display_fi_last: Optional[str]
    player_slug: Optional[str]
    position: Optional[str]
    comment: Optional[str]
    jersey_num: Optional[int]
    minutes: Optional[str]

    fgm: Optional[int]
    fga: Optional[int]
    fg_pct: Optional[float]
    fg3m: Optional[int]
    fg3a: Optional[int]
    fg3_pct: Optional[float]
    ftm: Optional[int]
    fta: Optional[int]
    ft_pct: Optional[float]
    o_reb: Optional[int]
    d_reb: Optional[int]
    reb: Optional[int]
    ast: Optional[int]
    stl: Optional[int]
    blk: Optional[int]
    tov: Optional[int]
    pf: Optional[int]
    pts: Optional[int]
    plus_minus_points: Optional[float]

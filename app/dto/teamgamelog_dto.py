from dataclasses import dataclass
from typing import Optional

@dataclass
class TeamGameLogDTO:

    # Attributs provenant de la base de données
    team_id: int
    game_id: str
    game_date: Optional[str] = None
    matchup: Optional[str] = None
    wl: Optional[str] = None
    w: Optional[int] = None
    l: Optional[int] = None
    w_pct: Optional[float] = None
    min: Optional[float] = None
    fgm: Optional[int] = None
    fga: Optional[int] = None
    fg_pct: Optional[float] = None
    fg3m: Optional[int] = None
    fg3a: Optional[int] = None
    fg3_pct: Optional[float] = None
    ftm: Optional[int] = None
    fta: Optional[int] = None
    ft_pct: Optional[float] = None
    oreb: Optional[int] = None
    dreb: Optional[int] = None
    reb: Optional[int] = None
    ast: Optional[int] = None
    stl: Optional[int] = None
    blk: Optional[int] = None
    tov: Optional[int] = None
    pf: Optional[int] = None
    pts: Optional[int] = None

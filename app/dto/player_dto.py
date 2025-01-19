from dataclasses import dataclass
from datetime import date
from typing import Optional, List

from app.dto.team_dto import TeamDTO


@dataclass
class PlayerDTO:

    # Attributs provenant de la base de données
    person_id: int = None
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
    games_played_current_season_flag: Optional[bool] = None
    greatest_75_flag: Optional[bool] = None
    draft_year: Optional[str] = None    # String car peut être Undrafted
    draft_round: Optional[str] = None   # String car peut être Undrafted
    draft_number: Optional[str] = None  # String car peut être Undrafted

    # Attributs relationnels
    team: Optional[TeamDTO] = None

    # Attributs fonctionnels
    moyenne_5_matchs: Optional[float] = None
    moyenne_10_matchs: Optional[float] = None
    moyenne_15_matchs: Optional[float] = None
    nombre_matchs_joues_30_jours: Optional[float] = None
    nombre_matchs_joues_30_jours_intervalle_1: Optional[float] = None
    nombre_matchs_joues_30_jours_intervalle_2: Optional[float] = None
    nombre_matchs_joues_30_jours_intervalle_3: Optional[float] = None
    nombre_matchs_joues_30_jours_intervalle_4: Optional[float] = None
    scores_5_derniers_matchs: Optional[List[float]] = None
    impact_back_to_back: Optional[float] = None
    nombre_back_to_back: Optional[float] = None
    impact_domicile: Optional[float] = None
    impact_exterieur: Optional[float] = None

    domicile_exterieur_match_plus_1: Optional[str] = None
    adv_match_plus_1: Optional[TeamDTO] = None
    impact_poste_adv_match_plus_1: Optional[float] = None
    precedents_scores_adv_match_plus_1: Optional[List[float]] = None

    domicile_exterieur_match_plus_2: Optional[str] = None
    adv_match_plus_2: Optional[TeamDTO] = None
    impact_poste_adv_match_plus_2: Optional[float] = None
    precedents_scores_adv_match_plus_2: Optional[List[float]] = None

    domicile_exterieur_match_plus_3: Optional[str] = None
    adv_match_plus_3: Optional[TeamDTO] = None
    impact_poste_adv_match_plus_3: Optional[float] = None
    precedents_scores_adv_match_plus_3: Optional[List[float]] = None

    domicile_exterieur_match_plus_4: Optional[str] = None
    adv_match_plus_4: Optional[TeamDTO] = None
    impact_poste_adv_match_plus_4: Optional[float] = None
    precedents_scores_adv_match_plus_4: Optional[List[float]] = None

    domicile_exterieur_match_plus_5: Optional[str] = None
    adv_match_plus_5: Optional[TeamDTO] = None
    impact_poste_adv_match_plus_5: Optional[float] = None
    precedents_scores_adv_match_plus_5: Optional[List[float]] = None

    def __repr__(self):
        # Permet d'afficher quelque chose de propre, en debug par exemple, plutôt que <dto.player_dto.PlayerDTO object at 0x1037b0c20>
        return f"PlayerDTO({self.person_id}, {self.first_name} {self.last_name}, {self.team_name})"

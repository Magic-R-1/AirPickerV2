class PlayerDTO:

    def __init__(self, person_id=None, first_name=None, last_name=None, display_first_last=None,
                 display_last_comma_first=None, display_fi_last=None, player_slug=None, birthdate=None,
                 school=None, country=None, last_affiliation=None, height=None, weight=None, season_exp=None,
                 jersey=None, position=None, roster_status=None, team_id=None, team_name=None,
                 team_abbreviation=None, team_code=None, team_city=None, player_code=None, from_year=None,
                 to_year=None, dleague_flag=None, nba_flag=None, games_played_flag=None, draft_year=None,
                 draft_round=None, draft_number=None):
        self.person_id = person_id
        self.first_name = first_name
        self.last_name = last_name
        self.display_first_last = display_first_last
        self.display_last_comma_first = display_last_comma_first
        self.display_fi_last = display_fi_last
        self.player_slug = player_slug
        self.birthdate = birthdate
        self.school = school
        self.country = country
        self.last_affiliation = last_affiliation
        self.height = height
        self.weight = weight
        self.season_exp = season_exp
        self.jersey = jersey
        self.position = position
        self.roster_status = roster_status
        self.team_id = team_id
        self.team_name = team_name
        self.team_abbreviation = team_abbreviation
        self.team_code = team_code
        self.team_city = team_city
        self.player_code = player_code
        self.from_year = from_year
        self.to_year = to_year
        self.dleague_flag = dleague_flag
        self.nba_flag = nba_flag
        self.games_played_flag = games_played_flag
        self.draft_year = draft_year
        self.draft_round = draft_round
        self.draft_number = draft_number

    def __repr__(self):
        # Permet d'afficher quelque chose de propre, en debug par exemple, plutôt que <dto.player_dto.PlayerDTO object at 0x1037b0c20>
        return f"PlayerDTO({self.person_id}, {self.first_name} {self.last_name}, {self.team_name})"

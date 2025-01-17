class TeamDTO:

    def __init__(self, team_id=None, full_name=None, abbreviation=None, nickname=None, city=None, state=None, year_founded=None):
        self.team_id = team_id
        self.full_name = full_name
        self.abbreviation = abbreviation
        self.nickname = nickname
        self.city = city
        self.state = state
        self.year_founded = year_founded

    def __repr__(self):
        # Affichage propre pour le débogage ou la journalisation
        return f"TeamDTO(id={self.team_id}, full_name={self.full_name}, abbreviation={self.abbreviation}, city={self.city})"

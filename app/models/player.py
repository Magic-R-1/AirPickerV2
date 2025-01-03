class Player:
    def __init__(self, player_id, name, team):
        self.player_id = player_id
        self.name = name
        self.team = team

    def __repr__(self):
        return f"Player({self.player_id}, {self.name}, {self.team})"

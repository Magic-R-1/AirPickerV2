class Team:
    def __init__(self, id, name, players=None):
        self.id = id
        self.name = name
        self.players = players or []

    def __repr__(self):
        return f"Team({self.id}, {self.name}, {self.players})"

    def add_player(self, player):
        self.players.append(player)

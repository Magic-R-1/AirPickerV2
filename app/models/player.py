import numpy as np

class Player:
    def __init__(self, id, name, team):
        self.id = id
        self.name = name
        self.team = team

    def __repr__(self):
        return f"Player({self.id}, {self.name}, {self.team})"

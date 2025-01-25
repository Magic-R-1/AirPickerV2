class PlayerNotFoundError(Exception):
    """Exception levée lorsqu'un joueur n'est pas trouvé."""
    pass

class TeamNotFoundError(Exception):
    """Exception levée lorsqu'une équipe n'est pas trouvée."""
    pass

class BoxscoreNotFoundError(Exception):
    """Exception levée lorsqu'une Boxscore n'est pas trouvée."""
    pass

class TeamGameLogNotFoundError(Exception):
    """Exception levée lorsqu'une TeamGameLog n'est pas trouvée."""
    pass

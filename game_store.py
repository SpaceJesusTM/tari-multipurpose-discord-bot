'''
Wordle User Game Managment
This part handles the game state management, allows each user to have their own active game.
'''
from wordle_types import ActiveGame


# Player Environment -> Mapping with User ID as key and game state as value
_player_env: dict[str, ActiveGame] = {}


def get_user_info(id: int) -> ActiveGame|None:
    """Return whether user is in an active game, or None otherwise."""
    return _player_env.get(str(id), None)


def set_user_info(id: int, info: ActiveGame):
    """Set the users status for when they are in a game."""
    _player_env[str(id)] = info

def clear_game(id: int):
    """Clear the users game from the Player Environment"""
    try:
        del _player_env[str(id)]
    except KeyError:
        pass

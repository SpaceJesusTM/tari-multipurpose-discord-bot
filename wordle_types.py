'''
Wordle Data Types
Data types used by the rest of the program.
'''
from enum import Enum
from dataclasses import dataclass, field

class LetterState(str, Enum):
    '''
    Result state for each letter position, showing whether it is correct, absent, or present.
        - Correct -> letter in correct place
        - Absent -> letter not in word
        - Present -> letter in word, not in correct place
    '''
    ABSENT = "absent"
    PRESENT = "present"
    CORRECT = "correct"

class EndResult(int, Enum):
    '''
    Current state of a user's active game.

    Can be either:
        - In the middle of PLAYING
        - Finished -> WON
        - Finished -> LOSE
        - Surrender needs no status
    '''
    PLAYING = 0
    WIN = 1
    LOSE = 2

@dataclass
class ActiveGame:
    '''
    Dataclass for the current state of a user's active game.

    Instance Attributes:
        - answer: A string representing the target word the user is guessing.
        - board_state: A list of strings represeting the guesses made so far.
        - results: List of tuple containg the Letter State class for the correct/present/absent 
                   results for each letter in each guess so far.
        - state: EndResult class representing whether the game is still running, has been won, or has been lost
    '''
    answer: str
    board_state: list[str] = field(default_factory=list)
    results: list[tuple[LetterState, ...]] = field(default_factory=list)
    state: EndResult = field(default=EndResult.PLAYING)

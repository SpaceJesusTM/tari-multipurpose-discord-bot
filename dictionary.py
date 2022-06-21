'''
Wordle Dictionary
This file gives fully cached access to the dictionary words.
'''
from pathlib import Path

# Read in txt files
solution_words = Path('data/solution_words.txt').read_text().splitlines()
accepted_words = Path('data/accepted_words.txt').read_text().splitlines()

def get_alphabet() -> str:
    return 'abcdefghijklmnopqrstuvwxyz'


def get_solution_words() -> list[str]:
    '''
    Return solution words.
    '''
    return solution_words


def get_acceptable_words() -> list[str]:
    '''
    Return acceptable guess words.
    '''
    return accepted_words

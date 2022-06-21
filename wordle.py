'''
Wordle Functions
All Wordle command functions called by bot in main.py
'''
###################################################################################################################################
# All Imports
import os
from typing import Callable

# Discord Python API
import discord
from discord.ext import commands

# Wordle Imports
from wordle_types import EndResult
from game_store import clear_game, get_user_info, set_user_info
from wordle_chat import begin_game, enter_guess, render_result
from dictionary import get_acceptable_words, get_alphabet, get_solution_words

###################################################################################################################################
# Wordle Functions
HELP_TEXT = """**Wordle is a Wordle-like clone that let's you play within Discord.**

Start a game by typing `$wordle <guess>` (replace <guess> with your word) and guess the word the game has secretly chosen. If Wordle returns a gray icon ⬛ the letter does not exist. If it returns a yellow icon 🟨 the letter exists but is on the wrong spot. If Wordle returns a green icon 🟩 the letter is on the correct spot.

New games are started automatically.

To re-show your current board type `$show`.
To give up use `$surrender`.
"""

async def handle_help(user: discord.User|discord.Member|None, reply: Callable):
    '''
    Show the help text.
    '''
    await reply(f"Hey {user.mention}, we got the help you need...", embed=discord.Embed(description=HELP_TEXT))


async def handle_show(user: discord.User|discord.Member, reply: Callable):
    '''
    Show the current board state.
    '''
    game = get_user_info(user.id)

    if game is None:
        await reply("You haven't started a game yet!")
        return

    guesses_left = 6 - len(game.board_state)

    # Render the results
    description = "Your board, you have " + str(guesses_left) + " guesses left: \n"
    description += "```"
    for result,word in zip(game.results, game.board_state):
        description += f"{render_result(result)} {word}\n"
    description += "```"

    await reply(description)


async def handle_surrender(user: discord.User | discord.Member, reply: Callable):
    '''
    Ends game and shows the player the answer.
    '''
    game = get_user_info(user.id)
    if game is None:
        await reply("You haven't started a game yet!")
        return

    answer = game.answer
    clear_game(user.id)

    await reply(f"You coward! 🙄\nYour word was `{answer}`!")


async def handle_new_guess(guess: str, user: discord.User|discord.Member, reply: Callable):
    '''
    Handles user guesses, if no game is going on a new one is started.
    '''
    # Validate input
    if not guess:
        await reply(f"To play Wordle simply type `$wordle <guess>` to start or continue your own personal game.")
        return

    guess = guess.lower() # formats user answer to lowercase
    guess = guess.removeprefix('guess:') # handles Discord mobile oddness
    if len(guess) != 5:
        await reply("Guess must be 5 letters long")
        return

    # Make sure the word is valid
    if guess not in get_solution_words() and guess not in get_acceptable_words():
        await reply("That's not a valid word!")
        return

    # Acumulator variable for text to return to the user
    description = ''

    # Make sure we have a game running, starting a new one if not
    game = get_user_info(user.id)
    if not game or game.state != EndResult.PLAYING:
        description += "Starting a new game, you have 6 guesses...\n"
        game = begin_game()
        set_user_info(user.id, game)

    # Make sure the user hasn't already guessed this word
    if guess in game.board_state:
        await reply("You've already guessed that word!")
        return

    # Make sure the guess uses only letters from the dictionary
    dictionary = get_alphabet()
    if any(char not in dictionary for char in guess):
        await reply(f"You can only use the following letters: `{dictionary}`")
        return

    # Process the guess
    enter_guess(guess, game)

    # Render the results
    guesses_left = 6 - len(game.board_state)
    description += "Your results so far, you have " + str(guesses_left) + " guesses left: \n"
    description += "```"
    for result,word in zip(game.results, game.board_state):
        description += f"{render_result(result)} {word}\n"
    description += "```"

    # See if the game is over
    if game.state == EndResult.WIN:
        description += f"\nCongratulations! 🎉\nCompleted in {len(game.board_state)} guesses!\n"
        clear_game(user.id)
    elif game.state == EndResult.LOSE:
        description += f"\nNo more guesses! 😭\nYour word was `{game.answer}`!\n"
        clear_game(user.id)

    # Send the response
    embed = discord.Embed(title="Wordle", description=description.strip('\n'))
    await reply(embed=embed)

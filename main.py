"""
Tari Bot 
Personal Discord bot for SPC

Features:
    Reactions
    Server Info
    Poll
    Random Choice Commands
    Eight Ball
    Tic Tac Toe
    Wordle
    YouTube Audio Streaming

Future Add Ons:
    Slash Commands
    More Games...
    Test commit

"""
###################################################################################################################################
# General Imports
import random
import discord
from discord.ext import commands, tasks

# Wordle Imports
from wordle import handle_new_guess, handle_help, handle_show, handle_surrender

# Music Imports
import wavelink
import datetime
import re

###################################################################################################################################
# Create the bot
bot = commands.Bot(command_prefix="$", help_command=None)


###################################################################################################################################
# General Commands and Reactions
@bot.event
async def on_ready():
    "Prints if Bot is connected to Discord server, sets status, and initalize node for Wavelink."
    print('Logged on as Tari#0734')
    bot.loop.create_task(node_connect())
    activity = discord.Game(name="$help for info...", type=3)
    await bot.change_presence(status=discord.Status.online, activity=activity)

@bot.event
async def on_message(message):
    """
    On response messages, bot will respond to any keyword found in any messages sent to the server.
    This is toggled on and off with $toggle_react
    """
    global response
    # Don't respond to ourselves
    if message.author == bot.user:
        return

    if 'ping' in message.content and response:
        await message.channel.send('pong')

    if 'pong' in message.content and response:
        await message.channel.send('ping')
    
    if 'night' in message.content and response:
        await message.channel.send('https://tenor.com/view/mochi-peach-cat-blanket-goma-gif-23380137')

    if 'morning' in message.content and response:
        await message.channel.send('https://tenor.com/view/good-morning-gif-25241728')

    message_lower = message.content.lower()
    if message.author == bot.user:
        return
    if message_lower.startswith('hello') and response:
        """
        Sends custom hello to specified user, else sends general hello.
        """
        if str(message.author) == '<Specific User Here>':
            await message.channel.send('Hello ' + str(message.author) + '!')
        else:
            await message.channel.send('Hello I am a test bot.')

    await bot.process_commands(message)

response = False

@bot.command(name='toggle_react')
async def message_on(ctx: commands.Context):
    """
    Toggle for above reactions.
    """
    global response

    if response:
        response = False
    else:
        response = True

    if response:
        await ctx.send(f'Tari will now respond.')
    else:
        await ctx.send(f'Tari will not respond.')

@bot.command(name='server')
async def server(ctx):
    """
    Sends embed with the server information of the server the bot is in.
    """
    name = str(ctx.guild.name)
    description = str(ctx.guild.description)
    owner = str(ctx.guild.owner)
    id = str(ctx.guild.id)
    founded = str(ctx.guild.created_at)
    member_count = str(ctx.guild.member_count)
    icon = str(ctx.guild.icon_url)

    # embed = discord.Embed(
    #     title=name + ' Server Information',
    #     description=description,
    #     color=discord.Colour.dark_blue()
    # )

    embed = discord.Embed(
    title=name + ' Server Information',
    color=discord.Colour.dark_blue()
    )

    embed.set_thumbnail(url=icon)
    embed.add_field(name="Owner", value=owner, inline=True)
    embed.add_field(name="Server ID", value=id, inline=True)
    embed.add_field(name="Est. Since", value=founded, inline=True)
    embed.add_field(name="Member Count", value=member_count, inline=True)

    await ctx.send(embed=embed)

@bot.command(name="poll")
async def create_poll(ctx, question: str, *options):
    """
    Sends embed with a poll and upto 10 options. Users are then able to participate via reactions.
    """
    if len(options) > 10:
        await ctx.send("You can only have a maximum of 10 options.")

    else:
        embed = discord.Embed(title="Poll",
                        description=str(question),
                        colour=discord.Colour.dark_blue())

        fields = [("Options", "\n".join([f"{numbers[idx]} {option}" for idx, option in enumerate(options)]), False),
                    ("Instructions", "React to cast a vote!", False)]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        message = await ctx.send(embed=embed)

        for emoji in numbers[:len(options)]:
            await message.add_reaction(emoji)

@bot.command(name='random_num')
async def random_num(ctx: commands.Context, start=1, end=10):
    """
    Random number generator, sends random number to chat.
    """
    if start > end:
        return await ctx.send('Please ensure start number is less than end number.')
    await ctx.send(f'Your random number is: `{random.randint(start, end)}`')

@bot.command(name='random_letter')
async def random_letter(ctx: commands.Context, options=26):
    """
    Random letter generator, sends random letter to chat.
    """
    if options < 1 or options > 26:
        return await ctx.send('Please choose a number between 1 and 26.')
    alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    letter = alphabet[random.randint(0, options - 1)]
    await ctx.send(f'Your random letter is: `{letter}`')

@bot.command(name='halp')
async def halp(ctx: commands.Context):
    """
    Multiple Choice letter generator.
    """
    alphabet = ['A', 'B', 'C', 'D', 'E']
    letter = alphabet[random.randint(0, 4)]
    await ctx.send(f'Stuck on a Question? :pray: Just choose: `{letter}`')

numbers = ("1️⃣", "2⃣", "3⃣", "4⃣", "5⃣",
		   "6⃣", "7⃣", "8⃣", "9⃣", "🔟")

@bot.command(name="8ball")
async def eight_ball(ctx, *, question: str):
    """
    Sends the users question with a random response from responses.
    """
    responses = ["It is certain.",
                    "It is decidedly so.",
                    "Without a doubt.",
                    "Yes - definitely.",
                    "You may rely on it.",
                    "As I see it, yes.",
                    "Most likely.",
                    "Outlook good.",
                    "Yes.",
                    "Signs point to yes.",
                    "Reply hazy, try again.",
                    "Ask again later.",
                    "Better not tell you now.",
                    "Cannot predict now.",
                    "Concentrate and ask again.",
                    "Don't count on it.",
                    "My reply is no.",
                    "My sources say no.",
                    "Outlook not so good.",
                    "Very doubtful."]
    await ctx.send(f':8ball: Question: {question}\n:8ball: Answer: {random.choice(responses)}')


###################################################################################################################################
# Help Commands
@bot.command(name="help")
async def help_command(ctx):
    """
    Sends embed with all commands.
    """
    embed = discord.Embed(title='All Commands:', color=discord.Colour.dark_blue())

    embed.add_field(name='General Commands (type: $general_help)', value='$toggle_react, $server, $poll,\n$random_num, $random_letter, \n$halp, $8ball', inline=False) 
    embed.add_field(name='Tic Tac Toe Commands (type: $ttt_help)', value='$tictactoe, $place', inline=False)
    embed.add_field(name='Wordle Commands (type: $wordle_help)', value='$wordle, $show, $surrender', inline=False)
    embed.add_field(name='Music Commands (type: $music_help)', value='$play, $search, $pause, $resume,\n$skip, $stop, $volume,\n$loop, $queue, $current', inline=False)
    
    return await ctx.send(embed=embed)

@bot.command(name="general_help")
async def help_general(ctx):
    """
    Sends embed with information of commands in General Commands.
    """
    embed = discord.Embed(title='General Commands:', color=discord.Colour.dark_blue())

    embed.add_field(name='`$toggle_react`', value="Turns on or off Tari's on-message responses.", inline=False)
    embed.add_field(name='`$server`', value="Gives Server Information.", inline=False)
    embed.add_field(name='`$poll <question> <option 1> <option 2>...`', value="Creates a poll with one question and up to 10 options. \n If question and options are multiple words, use \"\" to contain them.", inline=False)
    embed.add_field(name='`$random_num <start> <end>`', value="Chooses a random <start> and <end>. \n<start> must be greater than <end>. Default values are 1 and 10.", inline=False)
    embed.add_field(name='`$random_letter <num>`', value="Chooses a random letter up to the <num>th letter. \nDefault chooses from the entire alphabet.", inline=False)
    embed.add_field(name='`$halp`', value="Stuck on a multiple choice question? Try $halp.", inline=False)
    embed.add_field(name='`$8ball <question>`', value="Ask a yes or no question, get an accurate response!", inline=False)

    return await ctx.send(embed=embed)

@bot.command(name="ttt_help")
async def help_ttt(ctx):
    """
    Sends embed with information of commands in Tic Tac Toe Commands.
    """
    embed = discord.Embed(title='Tic Tac Toe Commands:', color=discord.Colour.dark_blue())

    embed.add_field(name='`$tictactoe <@player1> <@player2>`', value="Starts a game of Tic Tac Toe. To start, @ yourself and another player. ", inline=False)
    embed.add_field(name='`$place <num>`', value="Place your move on the corrseponding square (1-9 left to right).", inline=False)
    embed.add_field(name='More Information:', value="Game must be played untill all squares are filled. \nTo start a new game any current game must be finished. ", inline=False)

    return await ctx.send(embed=embed)

@bot.command(name="music_help")
async def help_music(ctx):
    """
    Sends embed with information of commands in Music Commands.
    """
    embed = discord.Embed(title='Music Commands:', color=discord.Colour.dark_blue())

    embed.add_field(name='`$play <song>`', value="Tari plays the given song or adds it to the queue if a song is already playing. \nCommand can take either the song URL or title. \nYouTube Playlist URL's currently do not work.", inline=False)
    embed.add_field(name='`$search <query>`', value="Tari searches for <query> on YouTube and returns the first 8 results. \nChosen track is then played or added to queue.", inline=False)
    embed.add_field(name='`$pause`', value="Pauses current song.", inline=False)
    embed.add_field(name='`$resume`', value="Resumes playing current song.", inline=False)
    embed.add_field(name='`$skip`', value="Skips playing current song.", inline=False)
    embed.add_field(name='`$stop`', value="Stops playing music and disconnects the bot. Queue is reset.", inline=False)
    embed.add_field(name='`$volume <num>`', value="Changes Tari's volume to <num> which must be between 1 and 150. \nDefault volume is 100 and volume is reset when bot is disconnected.", inline=False)
    embed.add_field(name='`$loop`', value="Enables or Disables the looping of the current song.", inline=False)
    embed.add_field(name='`$queue`', value="Displays all the songs in the queue. Bot disconnects once queue is empty.", inline=False)
    embed.add_field(name='`$current`', value="Displays the current playing song and status of Tari's music functions.", inline=False)

    return await ctx.send(embed=embed)


###################################################################################################################################
# Tic Tac Toe Commands
player1 = ""
player2 = ""
turn = ""
gameOver = True

board = []

winCon = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],
        [8, 4, 8],
        [2, 4, 6],
        ]

@bot.command(name="tictactoe")
async def tictactoe(ctx, p1: discord.Member, p2: discord.Member):
    """
    Begins a game of tic tac toe with p1 and p2.
    """
    global count
    global player1
    global player2
    global turn
    global gameOver

    if gameOver:
        global board
        board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:"]
        turn = ""
        gameOver = False
        count = 0

        player1 = p1
        player2 = p2

        line = ""
        for x in range(len(board)):
            if x == 2 or x == 5 or x == 8:
                line += " " + board[x]
                await ctx.send(line)
                line = ""
            else:
                line += " " + board[x]

        num = random.randint(1, 2)
        if num == 1:
            turn = player1
            await ctx.send("It is <@" + str(player1.id) + ">'s turn.")
        elif num == 2:
            turn = player2
            await ctx.send("It is <@" + str(player2.id) + ">'s turn.")
    else:
        await ctx.send("A game is already in progress! Finish it before starting a new one.")

@bot.command(name="place")
async def place(ctx, pos: int):
    """
    Makes a move for player corresponding to their turn and the state  of the board.
    Announces if game is won or tied.
    """
    global turn
    global player1
    global player2
    global board
    global count
    global gameOver

    if not gameOver:
        mark = ""
        if turn == ctx.author:
            if turn == player1:
                mark = ":regional_indicator_x:"
            elif turn == player2:
                mark = ":o2:"
            if 0 < pos < 10 and board[pos - 1] == ":white_large_square:" :
                board[pos - 1] = mark
                count += 1

                line = ""
                for x in range(len(board)):
                    if x == 2 or x == 5 or x == 8:
                        line += " " + board[x]
                        await ctx.send(line)
                        line = ""
                    else:
                        line += " " + board[x]

                checkWinner(winCon, mark)
                print(count)
                if gameOver == True:
                    await ctx.send(mark + " wins!")
                elif count >= 9:
                    gameOver = True
                    await ctx.send("It's a tie!")

                if turn == player1:
                    turn = player2
                elif turn == player2:
                    turn = player1
            else:
                await ctx.send("Be sure to choose an integer between 1 and 9 (inclusive) and an unmarked tile.")
        else:
            await ctx.send("It is not your turn.")
    else:
        await ctx.send("Please start a new game using the $tictactoe command.")

def checkWinner(winCon, mark):
    global gameOver
    for condition in winCon:
        if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
            gameOver = True

@tictactoe.error
async def tictactoe_error(ctx, error):
    print(error)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please mention 2 players for this command.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure to mention/ping players (ie. <@player2>).")

@place.error
async def place_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please enter a position you would like to mark.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure to enter an integer.")


###################################################################################################################################
# Wordle Commands
@bot.command(name='wordle', description='Guess a word in your own personal Wordle game!')
async def wordle_prefix(ctx: commands.Context, guess=''):
    """
    Begins and takes guesses for Wordle game.
    """
    await handle_new_guess(guess, ctx.author, ctx.reply)

@bot.command(name='surrender', help="Give up and reveal the word!")
async def surrender_prefix(ctx: commands.Context):
    """
    Ends current running game and gives answer.
    """
    await handle_surrender(ctx.author, ctx.reply)

@bot.command(name='wordle_help', help="How to play Wordle")
async def help_prefix(ctx: commands.Context):
    """
    Sends embed with information of commands in Wordle Commands.
    """
    await handle_help(ctx.author, ctx.reply)

@bot.command(name='show', help="Show current board state")
async def show_prefix(ctx: commands.Context):
    """
    Shows current state of the game and how many guesses are left.
    """
    await handle_show(ctx.author, ctx.reply)


###################################################################################################################################
# Music Commands
"""
Global Variables used to keep track of loop and volume status. 
"""
global_volume = 100
loop = False

@bot.event
async def on_wavelink_node_ready(node: wavelink.Node):
    """Prints if node is up and running."""
    print(f"Node {node.identifier} is ready!")

async def node_connect():
    """
    Creates node and connects to server.
    """
    await bot.wait_until_ready()
    # May need to look up for info on nodes
    await wavelink.NodePool.create_node(bot=bot, 
                                        host='host', 
                                        port=443, 
                                        password='password', 
                                        https=True)

@bot.event
async def on_wavelink_track_end(player: wavelink.Player, track: wavelink.Track, reason):
    """
    Handles events on track end. 
    Bot either:
        Loops current song if loop is enabled
        Disconnects from VC if queue is empty
        Plays the next song in the queue
    Call is made to nowplaying() to inform the user on the current playing song.
    """
    global loop
    ctx = player.ctx
    vc: player = ctx.voice_client

    if vc.loop:
        loop = True
        return await vc.play(track)
    
    if vc.queue.is_empty:
        return await vc.disconnect()

    next_song = vc.queue.get()
    await vc.play(next_song)
    await nowplaying(ctx)
    # await ctx.send(f'Now Playing: `{next_song.title}`')
    # await ctx.send(f'{next_song.thumbnail}')

URL_REGEX = re.compile(r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)+(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))")

@bot.command(name="play")
async def play(ctx: commands.Context, *, search: str):
    """
    Searches YouTube and plays the song given in search. Call is made to nowplaying() to inform the user on the current playing song.
    If a song is already playing, adds the searched song to queue.
    Can take both the song title and link. Does not work with YouTube playlist links.

    Most following music commands including this one have:
        Warning if the user is not in a Voice channel
        Notification that there is no music playing or that a track is not found.
    """
    global loop

    name = search

    if not getattr(ctx.author.voice, "channel", None):
        return await ctx.send('You are not in a voice channel, please enter VC and try again!')
    elif not ctx.voice_client:
        vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
    else:
        vc: wavelink.Player = ctx.voice_client
    
    if vc.queue.is_empty and not vc.is_playing():
        if URL_REGEX.match(search):
            tracks = await wavelink.NodePool.get_node().get_tracks(wavelink.YouTubeTrack, search)
            search = tracks[0]
        else:
            query = f'ytsearch: {search}'
            tracks = await wavelink.NodePool.get_node().get_tracks(wavelink.YouTubeTrack, query)
            search = tracks[0]
        
        if not tracks:
            return await ctx.send(f'No tracks found for `{name}`')

        await vc.play(search)
        # await ctx.send(f'Now Playing: `{search.title}`')
        # await ctx.send(f'{search.thumbnail}')
        loop = False
        vc.ctx = ctx
        setattr(vc, "loop", False)
        await nowplaying(ctx)

    else:
        if URL_REGEX.match(search):
            tracks = await wavelink.NodePool.get_node().get_tracks(wavelink.YouTubeTrack, search)
            search = tracks[0]
        else:
            query = f'ytsearch: {search}'
            tracks = await wavelink.NodePool.get_node().get_tracks(wavelink.YouTubeTrack, query)
            search = tracks[0]

        if not tracks:
            return await ctx.send(f'No tracks found for `{name}`')

        await vc.queue.put_wait(search)
        await ctx.send(f'Added to Queue: `{search.title}`')
        # await ctx.send(f'{search.thumbnail}')

@bot.command(name="search")
async def search(ctx: commands.Context, *, search: str):
    """
    Searches for 8 tracks from YouTube using search and awaits user response for song.
    Search is then cancelled, played, or added to queue.
    If playing, call is made to nowplaying() to inform the user on the current playing song.
    Search does not handle URLs.
    """
    global loop

    name = search

    if not getattr(ctx.author.voice, "channel", None):
        return await ctx.send('You are not in a voice channel, please enter VC and try again!')
    elif not ctx.voice_client:
        vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
    else:
        vc: wavelink.Player = ctx.voice_client
    
    if vc.queue.is_empty and not vc.is_playing():
        query = f'ytsearch: {search}'
        tracks = await wavelink.NodePool.get_node().get_tracks(wavelink.YouTubeTrack, query)
        search = tracks[0:8]

        if not tracks:
            return await ctx.send(f'No tracks found for `{name}`')

        embed = discord.Embed(title='Search Results (Type 1-8 for Track or 9 to Cancel Search):', color=discord.Colour.dark_blue())
        song_count = 0
        for song in search:
            song_count += 1
            embed.add_field(name=f'Track {song_count})', value=f'Track: `{song.title}` \nDuration: `{str(datetime.timedelta(seconds=song.length))}` \nURL: {song.uri}', inline=False) 
        
        await ctx.send(embed=embed)

        def check(m):
            return m.author.id == ctx.author.id
        
        response = 0
        possible_nums = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        while response == 0 or response.content not in possible_nums:
            response = await bot.wait_for('message', check=check)
            if response.content not in possible_nums:
                await ctx.send('Invalid Input Please Type a Number From 1-9...')

        if response.content == '9':
            return await ctx.send('Search Canceled...')
            
        track = search[int(response.content) - 1]

        await vc.play(track)
        # await ctx.send(f'Now Playing: `{search.title}`')
        # await ctx.send(f'{search.thumbnail}')
        loop = False
        vc.ctx = ctx
        setattr(vc, "loop", False)
        await nowplaying(ctx)

    else:
        query = f'ytsearch: {search}'
        tracks = await wavelink.NodePool.get_node().get_tracks(wavelink.YouTubeTrack, query)
        search = tracks[0:8]

        if not tracks:
            return await ctx.send(f'No tracks found for `{name}`')

        embed = discord.Embed(title='Search Results (Type 1-8 for Track or 9 to Cancel Search):', color=discord.Colour.dark_blue())
        song_count = 0
        for song in search:
            song_count += 1
            embed.add_field(name=f'Track {song_count})', value=f'Track: `{song.title}` \nDuration: `{str(datetime.timedelta(seconds=song.length))}` \nURL: {song.uri}', inline=False) 
        
        await ctx.send(embed=embed)

        def check(m):
            return m.author.id == ctx.author.id
        
        response = 0
        possible_nums = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        while response == 0 or response.content not in possible_nums:
            response = await bot.wait_for('message', check=check)
            if response.content not in possible_nums:
                await ctx.send('Invalid Input Please Type a Number From 1-9...')

        if response.content == '9':
            return await ctx.send('Search Canceled...')
            
        track = search[int(response.content) - 1]

        await vc.queue.put_wait(track)
        await ctx.send(f'Added to Queue: `{track.title}`')
        # await ctx.send(f'{search.thumbnail}')

@bot.command(name="pause")
async def pause(ctx: commands.Context):
    """
    Pauses current playing song or informs user otherwise.
    """
    if not getattr(ctx.author.voice, "channel", None):
        return await ctx.send('You are not in a voice channel, please enter VC and try again!')
    if not ctx.voice_client:
        return await ctx.send('No music currently playing...')

    node = wavelink.NodePool.get_node()
    player = node.get_player(ctx.guild)
    await player.pause()

@bot.command(name="resume")
async def resume(ctx: commands.Context):
    """
    Resumes current playing song or informs user otherwise.
    """
    if not getattr(ctx.author.voice, "channel", None):
        return await ctx.send('You are not in a voice channel, please enter VC and try again!')
    if not ctx.voice_client:
        return await ctx.send('No music currently playing...')

    node = wavelink.NodePool.get_node()
    player = node.get_player(ctx.guild)
    await player.resume()

@bot.command(name="stop")
async def stop(ctx: commands.Context):
    """
    Disconnects bot from voice channel resetting queue and volume, or informs user otherwise.
    """
    global global_volume
    if not getattr(ctx.author.voice, "channel", None):
        return await ctx.send('You are not in a voice channel, please enter VC and try again!')
    # if not ctx.voice_client:
    #     return await ctx.send('No music currently playing...')

    # await player.stop()
    global_volume = 100
    node = wavelink.NodePool.get_node()
    player = node.get_player(ctx.guild)
    await player.disconnect()

@bot.command(name="skip")
async def end_track(ctx: commands.Context):
    """
    Ends current playing song, skipping it, or informs user otherwise.
    """
    if not getattr(ctx.author.voice, "channel", None):
        return await ctx.send('You are not in a voice channel, please enter VC and try again!')
    if not ctx.voice_client:
        return await ctx.send('No music currently playing...')

    node = wavelink.NodePool.get_node()
    player = node.get_player(ctx.guild)
    await player.stop()

@bot.command(name="volume")
async def volume(ctx: commands.Context, vol: int):
    """
    Changes the volume of the bot to a value between 1-150, or informs user otherwise.
    """
    global global_volume

    if not getattr(ctx.author.voice, "channel", None):
        return await ctx.send('You are not in a voice channel, please enter VC and try again!')
    if not ctx.voice_client:
        return await ctx.send('No music currently playing...')
        
    if vol > 151 or vol < 0:
        return await ctx.send('Invalid Volume Input. Please enter a number between 1 and 150.')

    global_volume = vol
    vol_float = vol * 0.01
    vol_float = max(vol_float, 0.001)
    node = wavelink.NodePool.get_node()
    player = node.get_player(ctx.guild)
    await player.set_volume(vol_float)
    return await ctx.send(f'Volume set to `{global_volume}`')

@bot.command(name="loop")
async def loop(ctx: commands.Context):
    """
    Enables or Disables looping of current song, or informs user otherwise.
    """
    global loop
    if not getattr(ctx.author.voice, "channel", None):
        return await ctx.send('You are not in a voice channel, please enter VC and try again!')
    if not ctx.voice_client:
        return await ctx.send('No music currently playing...')

    vc: wavelink.Player = ctx.voice_client
    try:
        vc.loop ^= True
    except Exception:
        setattr(vc, "loop", False)
    if vc.loop:
        loop = True
        return await ctx.send('Loop Enabled')
    else:
        loop = False
        return await ctx.send('Loop Disabled')

@bot.command(name="queue")
async def queue(ctx: commands.Context):
    """
    Sends embed with information on all songs in the queue, or informs user otherwise.
    """
    if not getattr(ctx.author.voice, "channel", None):
        return await ctx.send('You are not in a voice channel, please enter VC and try again!')
    if not ctx.voice_client:
        return await ctx.send('No music currently playing...')

    vc: wavelink.Player = ctx.voice_client

    embed = discord.Embed(title='Queue:', color=discord.Colour.dark_blue())
    queue = vc.queue.copy()
    song_count = 0
    for song in queue:
        song_count += 1
        embed.add_field(name=f'Track {song_count})', value=f'Track: `{song.title}` \nChannel: `{song.author}` \nDuration: `{str(datetime.timedelta(seconds=song.length))}` \nURL: {song.uri}', inline=False) 
    if song_count == 0:
        embed.add_field(name='Queue Empty...', value=' Use "play" command to add song.', inline=False)

    return await ctx.send(embed=embed)

@bot.command(name="current")
async def nowplaying(ctx: commands.Context):
    """
    Sends embed with the song title (and URL), YouTube channel, Volume of the bot, and the status of looping.
    The tracks thumbnail is also displayed if it is avalible.
    Bug in Wavelink library causes the thumbnail to disapear if a track is looped. 
    """
    global global_volume, loop
    if not getattr(ctx.author.voice, "channel", None):
        return await ctx.send('You are not in a voice channel, please enter VC and try again!')
    if not ctx.voice_client:
        return await ctx.send('No music currently playing...')

    vc: wavelink.Player = ctx.voice_client

    if not vc.is_playing():
        return await ctx.send('No music currently playing...')
    
    embed = discord.Embed(title="Now Playing:", 
                        description=f"[{vc.track.title}]({str(vc.track.uri)})",
                        color=discord.Colour.dark_blue())

    if type(vc.track) is wavelink.YouTubeTrack:
        embed.set_thumbnail(url=vc.track.thumbnail)
    embed.add_field(name="Duration", value=f"{str(datetime.timedelta(seconds=vc.track.length))}", inline=True)
    embed.add_field(name="Channel", value=vc.track.author, inline=True)
    embed.add_field(name="Volume", value=str(global_volume), inline=False)
    if loop:
        embed.add_field(name="Loop", value='Enabled', inline=False)
    else:
        embed.add_field(name="Loop", value='Disabled', inline=False)

    return await ctx.send(embed=embed)


###################################################################################################################################
# Bot Token and Run Start
if __name__ == "__main__":
    """
    To run bot replace token with the token of your bot (given when an application/bot is created).
    https://discord.com/developers/docs/intro
    """
    bot.run('TOKEN')

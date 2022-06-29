# tari-multipurpose-discord-bot
A discord bot created using discord.py which centralizes a variety of commands from different popular bots.

All Commands:
- $toggle_react: Turns on or off Tari's on-message responses.
- $server: Gives Server Information.
- $poll <question> <option 1> <option 2>...: Creates a poll with one question and up to 10 options. If question and options are multiple words, use "" to contain them.
- $random_num <start> <end>: Chooses a random <start> and <end>. <start> must be greater than <end>. Default values are 1 and 10.
- $random_letter <num>: Chooses a random letter up to the <num>th letter. \nDefault chooses from the entire alphabet.
- $halp: Stuck on a multiple choice question? Try $halp.
- $8ball <question>: Ask a yes or no question, get an accurate response!
- $wordle <guess>: Start and make guesses for a game of Wordle.
- $show: Show state of the current Wordle game.
- $surrender: End the current Wordle game and reveal answer.
- $tictactoe <@player1> <@player2>: Starts a game of Tic Tac Toe. To start, @ yourself and another player.
- $place <num>: Place your move on the corrseponding square (1-9 left to right).
- $play <song>: Tari plays the given song or adds it to the queue if a song is already playing. Command can take either the song URL or title. YouTube Playlist URL's currently do not work.
- $search <query>: Tari searches for <query> on YouTube and returns the first 8 results. Chosen track is then played or added to queue.
- $pause: Pauses current song.
- $resume: Resumes playing current song.
- $skip: Skips playing current song.
- $stop: Stops playing music and disconnects the bot. Queue is reset.
- $volume <num>: Changes Tari's volume to <num> which must be between 1 and 150. Default volume is 100 and volume is reset when bot is disconnected.
- $loop: Enables or Disables the looping of the current song.
- $queue: Displays all the songs in the queue. Bot disconnects once queue is empty.
- $current: Displays the current playing song and status of Tari's music functions.

To utilize bot...
- Create an application (bot) on the Discord developer site and locate the token, replace 'TOKEN' at the bottom of main.py.
- Replace the fields in node_connect() with a valid Lavalink (Wavelink) server (ie: https://www.freelavalink.ga/ or create/host your own server).
- Invite the bot to your server using the Discord developer site.

*There are many tutorials if you get stuck or would like more information on this process.
  
Credit to...
- https://www.youtube.com/watch?v=SS_RU2Slh-M&list=PLJXEdhN0Tc3LRT716enS1LcY4OF8vg1VA&index=5 - for tutorials on utilizing the discord.py Library as well as tutorials on the Server Info. and Tic Tac Toe commands.
- https://www.youtube.com/watch?v=_1DKYyFniNk&list=PLW4Cg4G29vz0enf3ZeqWPPd_-Z3YK8mH4&index=21 - for tutorials on how to implement and utilize the Wavelink Library.
- https://thecodingchannel.hashnode.dev/full-tutorial-we-build-a-python-wordle-clone-discord-bot-with-disnake#heading-1-set-up-a-folder-for-your-project - for tutorial on how to implement Wordle in a Discord bot format.
  

## Two of These People Are Lying
## A game by Tom Scott and the Technical Difficulties
## Adapted for Discord by Sam Ettinger ettingersam@gmail.com

import random
import unicodedata
from games import config

# Set up new entry for games config file
gameDict = {}
gameDict['intro'] = '''
Each game consists of multiple rounds. In each game, there is a dedicated guesser; everyone else is a player. Before starting a round, every player submits the title of a Wikipedia article by DMing it to the games bot. When the round begins, the bot announces one of the Wikipedia articles at random. It is then up to each player to convince the guesser that they were the one who read and submitted that Wikipedia article. Of course, only one player knows the actual contents of the Wikipedia article; the other players have to bluff!

The guesser must choose which player they think is telling the truth. If the guesser guesses correctly, both the guesser and the picked player get a point. If the guesser guesses incorrectly, the person they guessed still gets a point.

After each round, one of the players (the one whose article was randomly picked) must submit a new Wikipedia article by DMing the games bot again.

Available in-game commands:
`$newgame` -- Starts a fresh game, discarding any stored players' submissions.
`$newround` -- Begins a round by picking a submission at random.
'''

# Set up game logic, initialization function, game commands
def init():
  config.players = {}
  config.playingGame = False
  
def normalized(string):
  decomp = unicodedata.normalize('NFD', string)
  return ''.join([letter for letter in decomp if ord(letter)<0x280]).upper()

async def newgame(message):
  config.playingGame = True
  config.players = {}
  await message.channel.send('Starting a new game! All entries have been cleared. DM the bot to submit your Wikipedia article title.')

async def newround(message):
  if not config.playingGame:
    return
  if len(config.players.keys()) > 0:
    # Pick one of the players' entries at random
    randoplayer = random.sample(list(config.players.keys()), 1)[0]
    randotopic = config.players[randoplayer]
    # Remove the rando player from the dictionary of submissions
    config.players.pop(randoplayer, None)
    # Reveal topic to the channel
    await message.channel.send(f"The topic is: `{randotopic}`")

async def DM(message):
  if not config.playingGame:
    return
  # Check if the message author *needs* a new topic
  if message.author.name in config.players.keys():
    await message.author.send(f"You already submitted the topic {config.players[message.author]}.")
  # Normalize the string, make it all-caps and add it to the list of topics
  else:
    config.players[message.author.name] = normalized(message.content)
    await message.author.send(f"Your topic `{config.players[message.author.name]}` has been recorded.")
    
gameDict['init'] = init
gameDict['$newgame'] = newgame
gameDict['$newround'] = newround
gameDict['DM'] = DM

# Add this game to the config file
config.loadedGames['Two of These People Are Lying'] = gameDict

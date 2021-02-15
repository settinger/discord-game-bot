## Chameleon
## A game by Big Potato Games
## Adapted for Discord by Sam Ettinger ettingersam@gmail.com

import random
from games import config

# The game data is in a separate file that I will *not* be putting online because it's the main content of the game that Big Potato is selling, so it's not right for me to hand it out for free
from games.chameleon_data import cards

# Set up new entry for games config file
gameDict = {}
gameDict['intro'] = '''
In each round, a list of sixteen related things is shown to all the players. One of these sixteen things is selected at random and DMed to all but one of the players. The remaining player merely knows that they are the Chameleon for this round! The Chameleon's goals are to (1) not get caught, (2) figure out what the subject is.

Players take turns saying a single word that relates to the thing they were given. The Chameleon has to bluff. After everyone has said their single word, the players can grill each other to get more details or explanations, while trying not to give away the subject of the round.

At the end of the discussion, players vote on who they think is the Chameleon. If the players guess incorrectly, the Chameleon wins! If the players guess correctly, the Chameleon gets to guess what the subject of the round was. If the Chameleon guesses correctly, they win! Otherwise, the other players all win.

Available in-game commands:
`$newgame` -- Starts a fresh game.
`$join` -- Tells the bot that you wish to play in this game.
`$newround` -- Begins a round with all the players that have joined.
'''

# Set up game logic, initialization function, game commands
def init():
  config.players = []
  config.cards = cards
  config.playingGame = False

def formatted(card):
  message = ''
  message += '**Category: ' + card[0].upper() + '**\n'
  for entry in card[1]:
    message += entry + '\n'
  return message

async def newGame(message):
  config.players = []
  config.playingGame = True
  await message.channel.send('Starting a new game! Type `$join` to be added to the game.')

async def join(message):
  if not config.playingGame:
    return
  if message.author not in config.players:
    config.players += [message.author]
    await message.channel.send(f"{message.author.name} has joined the game.")

async def newRound(message):
  if not config.playingGame:
    return
  chosenCard = random.sample(config.cards, 1)[0]
  # message the channel with the chosen card
  await message.channel.send(formatted(chosenCard))

  # Pick the secret and the chameleon
  secret = random.sample(chosenCard[1], 1)[0]
  random.shuffle(config.players)
  chameleon = config.players[0]

  # DM each player
  await chameleon.send('You are the chameleon!')
  for player in config.players[1:]:
    await player.send(f"The secret topic is: **{secret}**")

gameDict['init'] = init
gameDict['$newgame'] = newGame
gameDict['$join'] = join
gameDict['$newround'] = newRound

# Add entry to games config file
config.loadedGames['Chameleon'] = gameDict

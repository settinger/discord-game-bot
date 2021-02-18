## Sam's Dumb Game Bot for Discord
## ettingersam@gmail.com
## February 2021

import discord
import os
from dotenv import load_dotenv
load_dotenv()

# Get each game that's available, plus the config file
from games import config, chameleon, twolying

# Initialize Discord client
client = discord.Client()

# Announce when client has logged in
@client.event
async def on_ready():
  print(f'Logged in as {client.user}')

# Read Discord messages and respond when needed
@client.event
async def on_message(message):
  # 1. If the message is from the bot itself, ignore message
  if message.author == client.user:
    return

  # 2. Set channel focus with $hello
  elif message.content.lower().startswith('$hello'):
    config.channelFocused = False
    config.channelFocus = message.channel
    await message.channel.send(f"Bot will only respond to $commands from {message.channel.name}.")

  # 3. Provide a list of commands that are available
  elif message.content.lower().startswith('$help') or message.content.lower().startswith('$commands'):
    await message.channel.send(config.game_details())

  # 4. Set the active game with $setgame
  elif message.content.lower().startswith('$setgame'):
    payload = message.content.lower()[9:]
    haveNewGame = setGame(payload)
    if haveNewGame:
      await message.channel.send(f"Active game has been set to **{config.currGame}**.")
    else:
      await message.channel.send(f"No game was found with that title. {config.available_games()}")

  # 5. Look up the $commands defined in the current game
  elif message.content.startswith('$') and message.content.lower() in config.currRules.keys():
    if (not config.channelFocused) or message.channel == config.channelFocus:
      await config.currRules[message.content.lower()](message)

  # 6. (Optional) Look up rules for being DMed by players
  elif 'DM' in config.currRules.keys() and isinstance(message.channel, discord.channel.DMChannel):
    await config.currRules['DM'](message)

# Set game
def setGame(payload):
  gameFound = False
  for game in config.loadedGames.keys():
    if game.lower().startswith(payload) or payload.startswith(game.lower()):
      gameFound = True
      config.currGame = game
      config.currRules = config.loadedGames[game]
  return gameFound
      
      

client.run(os.getenv('DISCORD_TOKEN'))

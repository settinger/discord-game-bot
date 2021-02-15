## Game Config File
## Begins by asserting no game is set up, and bot listens to every channel. This gets re-written when games get loaded in

channelFocused = False
channelFocus = None
currGame = 'none'
currRules = {}
loadedGames = {'none': {}}

# List all available games
def available_games():
  return f"Available games are: {', '.join([f'**{game}**' for game in loadedGames.keys() if game!='none'])}."

# List the currently loaded game
def game_details():
  if currGame == 'none':
    return "No game is active at the moment. Pick a game with `$setgame {gamename}.`\n" + f"{available_games()}"
  else:
    return f"Active game is **{currGame}**." + "\n\n" + f"{loadedGames[currGame][intro]}" + "\n\nOther available bot commands:\n`$setgame {gamename}` -- Changes the active game.\n`$help` -- shows this page."

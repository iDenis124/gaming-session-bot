import datetime

# stopTime = datetime.strptime('05:00:00', '%H:%M:%S')
gameTime = datetime.datetime(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day, 20, 00, 00)
noGameMessage = "nothing yet"
emojis = ["👍", "❓"]
helpCommand = """
- `?hostgame` sends a message which asks who can play with the reaction system
- `?endhost` for manually ending the current session
- `?cancelhost` if there aren't enough people, will also ping the game role to announce it
- Both `?cancelhost` and `?endhost` can only be used by Amy and whoever made the current session
- `?time` Shows the remaining time until the game session
- `?help` what you're reading rn lol
"""

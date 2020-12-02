# Game session bot
This is a discord bot for hosting game sessions, like Among Us
# How to use it
## Actually installing it
You need the following:
- Python 3 or later
- [discord.py](https://github.com/Rapptz/discord.py)
- An environment variable called `BOTTOKEN` containing the token
## Configuring it
In `games.py` you can find the example games, made of python dictionaries, with the game's name, the server's channel where the game talk will happen, and the role which the bot will ping\
There is also a list with all of the dictionaries names, both need to be updated
## Using the bot
There are 3 simple commands
- ?hostgame
- ?cancelhost
- ?endhost
- ?time
There is also `?help` if you forget the commands
### ?hostgame
Starts a session and updates the status to reflect that, blocks new session to prevent overlaps\
It will also ping again 10 minutes before the set time, and 10 after with only the people that didn't join the VC 
### ?endhost
To be used after the session, to clear the status and make other session possible\
NOTE: This also happens by itself at 5 AM, configurable in `settings.py`
### ?cancelhost
Like `?endhost`, but only if there aren't enough people avaliable to play
### ?time
It tells the remaining time until the current session starts
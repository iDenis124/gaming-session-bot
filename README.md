# Game session bot
This is a discord bot for hosting game sessions, like Among Us
# How to use it
This is meant to be run on a 24/7 linux server
## Actually installing it
You need the following:
- Python 3 or later
- discord.py module
This should already be included under venv/Lib/discord, but when it was first used it didn't work. If you have any idea on how to fix this, please do send a pr
- An environment variable called `BOTTOKEN` containing the token
## Configuring it
In `games.py` you can find the example games, made of python dictionaries, with the game's name, the server's channel where the game talk will happen, and the role which the bot will ping
There is also a list with all of the dictionaries names, both need to be updated
## Using the bot

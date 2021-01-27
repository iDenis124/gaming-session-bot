# Game session bot
This is a Discord bot for hosting game sessions
## Installing it
You need the following:
- Python 3.x (made with 3.8 in mind)
- [discord.py](https://github.com/Rapptz/discord.py)
- An environment variable called `BOTTOKEN` containing the token  
Copy both `bot.py` and `settings.py` in a folder (copy from `src` not `example`)
## Configuring it
Now we need to set `settings.py` up so the bot can function
### Adding Games
In the first 5 lines, you will find the template for a game  
Copy it for how many games you want  
- `name` with the game name
- `channelID` with the id of the channel where it will host the session
- `roleID` the role it pings
- Adding to `gameList` all the games you just added
### Other settings
- `allRoles` what roles to add when
- `noGameMessage` the status message displayed when no session is planned
- `sessionRightNowMessage` what gets appended after the game name when the session is play
- `joinMessage` what the bot DMs a new user when they join  
Leave empty for no DM
- `emojis` the bot only cares about the first two emojis, but you can add as many as you like  
To get what you put in, go into discord, type the emoji, then add `\` before and send the message  
Copy that and put it here
- `emojisName` now the name of the emoji
- `sessionVCID` the ID of the voice channel where people connect during the game session  
- `timezone` after you make a session and before it starts, the bot status will say what time the session is at  
This gets added after it
- `bannedUsers` add here the ID's of anyone who should not use the bot, i.e people that spam sessions to mass ping
- `sessionTime` this is the default time the session happens at
---
## Using the bot
- `?hostgame`
- `?cancelhost`
- `?endhost`
- `?status`
- `?time`
- `?updatesettings` **ADMIN ONLY**
- `?addrole` **ADMIN ONLY**
- `?removerole` **ADMIN ONLY**  
### ?hostgame
- `?hostgame` Starts a session with the game name and default time
- `?hostgame 20:00` Starts a session with the game name and specified time
- `?hostgame 20:00 lorem ipsum` Starts a session with the specified time and text  
It will also send a message that users need to react to join in  
The first emoji is for *I am sure I will join* and the second one is for *I might join*  
People who reacted with the first one will be pinged if they did not join the VC 10 minutes after it started
### ?endhost
To be used after the session ended, to clear the status and allow for other sessions
### ?cancelhost
Like `?endhost`, but only usable before the session starts and it will ping those to reacted with the first emoji telling them it got canceled
### ?status
Shows who is joining
### ?time
Time remaining until the session starts
#### ?updatesettings
For adding a game to `settings.py` but without restarting the bot
### The following two work in an opt-out system, where someone gets every role and specifies which they would like to keep
#### ?addrole (broken currently)
When making a new game, to give everyone the new role
#### ?removerole (broken currently)
Removing a game role from everyone who has it

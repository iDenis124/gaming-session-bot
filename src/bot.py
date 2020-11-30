import discord
import os
import games
import settings
import time
import datetime
# import threading

class MyClient(discord.Client):
    async def on_ready(self):
        print("Logged on as", self.user)
        await client.change_presence(activity=discord.Game(name=settings.noGameMessage))

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.lower() == "?hostgame":
            games.gameCheck = 0
            games.sessionOwner = message.author.id
            if games.currentGame == "":
                global game, messageWithPing
                for game in games.gameList:
                    if message.channel.id == game["channelID"]:
                        messageWithPing = await message.channel.send(
                            "<@&{0}> session at 20:00 CET?".format(game["roleID"]))
                        for emoji in settings.emojis:
                            await messageWithPing.add_reaction(emoji)
                        await client.change_presence(activity=discord.Game(name=game["name"]))
                        games.currentGame = game
                        await messageWithPing.pin()
                    else:
                        games.gameCheck = games.gameCheck + 1
                        if games.gameCheck == len(games.gameList):
                            await message.channel.send("This isn't a game channel!")
                        else:
                            continue
            else:
                await message.channel.send("{0} is already in session!".format(games.currentGame["name"]))

        if message.content.lower() == "?endhost" and (
                message.author.id == 108530201708773376 or message.author.id == games.sessionOwner):
            await message.channel.send("Game session has ended!")
            await messageWithPing.unpin()
            await client.change_presence(activity=discord.Game(name=settings.noGameMessage))
            games.currentGame = ""

        if message.content.lower() == "?cancelhost" and (
                message.author.id == 108530201708773376 or message.author.id == games.sessionOwner):
                #
                #
                # MAKE IT ONLY PING PEOPLE WHO REACTED WITH THE THUMBS UP
                #
                #
            await message.channel.send("<@&{0}> session has been canceled!".format(games.currentGame["roleID"]))
            await messageWithPing.unpin()
            await client.change_presence(activity=discord.Game(name=settings.noGameMessage))
            games.currentGame = ""

        if message.content.lower() == "?time":
            minutes = int(secondsUntilTime(settings.gameTime) / 60)
            if minutes <= 0:
                await message.channel.send("The session already started!")
            else:
                hours = 0
                while minutes >= 60:
                    minutes = minutes - 60
                    hours = hours + 1
                if hours == 0:
                    await message.channel.send("{0} minutes remaining until the game session!".format(int(minutes)))
                else:
                    await message.channel.send("{0} hours and {1} minutes remaining until the game session!".format(
                        int(minutes / 60),
                        int(minutes))
                        )

        if message.content.lower() == "?help":
            await message.channel.send(settings.helpCommand)

def secondsUntilTime(val2):
    return (val2 - datetime.datetime.now()).total_seconds()

# exitFlag = 0
#
#
# class myThread(threading.Thread):
#     def __init__(self, threadID, name, counter):
#         threading.Thread.__init__(self)
#         self.threadID = threadID
#         self.name = name
#         self.counter = counter
#
#     def run(self):
#         clearStatus()

client = MyClient()
client.run(os.environ["BOTTOKEN"])
# clearStatusThread = myThread(1, "5 AM Timer", 1)
# clearStatusThread.start()

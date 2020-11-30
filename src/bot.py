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
            await message.channel.send("<@&{0}> session has been canceled!".format(games.currentGame["roleID"]))
            await messageWithPing.unpin()
            await client.change_presence(activity=discord.Game(name=settings.noGameMessage))
            games.currentGame = ""

        if message.content.lower() == "?time":
            timeRemaining = str(datetime.timedelta(
                seconds=dateDiffInSeconds(int(time.time()), settings.gameTime)))
            await message.channel.send("{0} remaining until the {1} session!".format(timeRemaining, games.currentGame))

        if message.content.lower() == "?help":
            await message.channel.send(settings.helpCommand)

def dateDiffInSeconds(dt2, dt1):
    timedelta = dt2 - dt1
    # return timedelta.days * 24 * 3600 + timedelta.seconds
    return timedelta.seconds

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

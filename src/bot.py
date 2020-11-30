import discord
import os
import games
import settings
# import time as timer
import time
import datetime


# from datetime import datetime as datetimer  # , time
# import threading


# async def botClearStatus():
#     await client.change_presence(activity=discord.Game(name=settings.noGameMessage))
#     games.currentGame = ""


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
            await client.change_presence(activity=discord.Game(name=settings.noGameMessage))
            # noinspection PyUnboundLocalVariable
            await messageWithPing.unpin()
            games.currentGame = ""

        if message.content.lower() == "?cancelhost" and (
                message.author.id == 108530201708773376 or message.author.id == games.sessionOwner):
            # noinspection PyTypeChecker
            await message.channel.send("<@&{0}> session has ended!".format(games.currentGame["roleID"]))
            await client.change_presence(activity=discord.Game(name=settings.noGameMessage))
            await messageWithPing.unpin()
            games.currentGame = ""

        if message.content.lower() == "?time":
            timeRemaining = str(datetime.timedelta(seconds=dateDiffInSeconds(int(time.time()), settings.gameTime)))
            await message.channel.send("{0} remaining until the {1} session!".format(timeRemaining, games.currentGame))
            # await message.channel.send("command is neat, but it apparently happens in 100+ years, and I won't fix it until KC Teaches Me Rust:tm:")

        if message.content.lower() == "?help":
            await message.channel.send(settings.helpCommand)


#
# def clearStatus():
#     botClearStatus()
#     print(dateDiffInSeconds(datetime.now(), settings.stopTime))
#     timer.sleep(100)
#     # timer.sleep(dateDiffInSeconds(datetime.now(), settings.stopTime))
#     clearStatus()
#
#
def dateDiffInSeconds(dt2, dt1):
    timedelta = dt2 - dt1
    # return timedelta.days * 24 * 3600 + timedelta.seconds
    return timedelta.seconds


# TODO: fix the time errors
#
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
#

client = MyClient()
# clearStatusThread = myThread(1, "Thread-1", 1)
# clearStatusThread.start()
client.run(os.environ["BOTTOKEN"])

import asyncio
import datetime
import os

import discord
from discord.ext import commands, tasks

import games
import settings

client = commands.Bot(command_prefix="?")


def seconds_until_time(val2):
    return (val2 - datetime.datetime.now()).total_seconds()


async def clear_status():
    await client.change_presence(activity=discord.Game(name=settings.noGameMessage))
    games.currentGame = ""
    games.currentSessionTime = ""
    games.sessionRightNow = 0
    games.sessionOwner = 0
    games.messageToPing = ""
    games.peopleWhoReacted = []
    games.peopleWhoReactedAndNotInVC = []
    games.peopleInVC = []


async def change_status(game, timeElectricBoogaloo, statusMessage):
    if statusMessage == "":
        await client.change_presence(activity=discord.Game(name="{0} | {1} CET".format(
            game["name"],
            timeElectricBoogaloo
        )))
    else:
        await client.change_presence(activity=discord.Game(name="{0} | {1} CET".format(
            statusMessage,
            timeElectricBoogaloo
        )))


@client.event
async def on_ready():
    print("Bot is ready")
    stop_session.start()
    change_status_at_session_start.start()
    await client.change_presence(activity=discord.Game(name=settings.noGameMessage))


@client.event
async def on_reaction_add(reaction, user):
    if str(reaction) == settings.emojis[0]:
        if user.id == settings.botID:
            pass
        else:
            games.peopleWhoReacted.append(user.id)


@client.event
async def on_reaction_remove(reaction, user):
    if str(reaction) == settings.emojis[0]:
        games.peopleWhoReacted.remove(user.id)


@client.command()
async def hostgame(ctx, timeTheTrilogy=settings.defaultGameTime.strftime("%H:%M"), *, statusMessage=""):
    if games.currentGame == "":
        gameCheck = 0
        for game in games.gameList:
            if game["channelID"] == ctx.channel.id:
                games.sessionOwner = ctx.author.id
                games.currentGame = game
                games.currentSessionTime = timeTheTrilogy
                await ctx.send("{0} session at {1} CET?".format(
                    game["name"],
                    timeTheTrilogy
                ))
                games.messageToPing = ctx.channel.last_message
                await games.messageToPing.pin()
                for emoji in settings.emojis:
                    await games.messageToPing.add_reaction(emoji)
                await change_status(game, timeTheTrilogy, statusMessage)
            else:
                gameCheck = gameCheck + 1
                if gameCheck == len(games.gameList):
                    await ctx.send("This isn't a game channel!")
                else:
                    continue
    else:
        await ctx.send("{0} is already in session!".format(games.currentGame["name"]))


@client.command()
async def endhost(ctx):
    if seconds_until_time(
        datetime.datetime(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day,
                          int(games.currentSessionTime[0:2]), int(games.currentSessionTime[3:6]), 00)) <= 0:
        await ctx.send("{0} has ended!".format(games.currentGame["name"]))
        await games.messageToPing.unpin()
        await clear_status()
    else:
        await ctx.send("Game session hasn't even started, you can't end it!")


@client.command()
async def cancelhost(ctx):
    if ctx.author.id in [108530201708773376, 277017606446252032, 337138856858222592, games.sessionOwner]:
        users = ""
        for x in games.peopleWhoReacted:
            users = users + "<@{0}> ".format(x)
        await ctx.send("{0}session has been canceled!".format(users))
        await games.messageToPing.unpin()
        await clear_status()
    else:
        await ctx.send("You can't cancel the current session, you aren't the person who made it!")
        await ctx.send("If the session is over, use `?endhost` instead!")


@client.command()
async def time(ctx):
    minutes = int(seconds_until_time(
        datetime.datetime(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day,
                          int(games.currentSessionTime[0:2]), int(games.currentSessionTime[3:6]), 00)) / 60)
    if minutes <= 0:
        await ctx.send("The session already started!")
    else:
        hours = 0
        while minutes >= 60:
            minutes = minutes - 60
            hours = hours + 1
        if hours == 0:
            await ctx.send("{0} minutes remaining until the game session!".format(int(minutes)))
        else:
            await ctx.send("{0} hours and {1} minutes remaining until the game session!".format(
                int(hours),
                int(minutes))
            )


@tasks.loop(seconds=int(seconds_until_time(settings.stopTime) + 86400))
async def stop_session():
    await clear_status()


@tasks.loop(seconds=10)
async def change_status_at_session_start():
    if games.currentGame == "":
        pass
    else:
        if games.sessionRightNow == 0:
            await asyncio.sleep(seconds_until_time(
                datetime.datetime(datetime.datetime.now().year, datetime.datetime.now().month,
                                  datetime.datetime.now().day,
                                  int(games.currentSessionTime[0:2]), int(games.currentSessionTime[3:6]), 00)) - 600)
            await games.messageToPing.channel.send("<@&{0}> in 10 minutes!".format(games.currentGame["roleID"]))
            await asyncio.sleep(600)
            await client.change_presence(
                activity=discord.Game(name="{0} is in session!".format(games.currentGame["name"])))
            playerCount = str(games.messageToPing.reactions)
            await games.messageToPing.channel.send(
                "<@&{0}> session started! There are `{1}` people who reacted with {2}".format(
                    games.currentGame["roleID"],
                    int(playerCount[109:110]) - 1,
                    settings.emojis[int(0)]
                ))
            games.sessionRightNow = 1
            await asyncio.sleep(600)
            games.peopleInVC = client.get_channel(settings.sessionVCID).voice_states.keys()
            print(games.peopleInVC)
            for user in games.peopleWhoReacted:
                if user in games.peopleInVC:
                    pass
                else:
                    if user < 10:
                        pass
                    else:
                        games.peopleWhoReactedAndNotInVC.append(user)
            users = ""
            for x in games.peopleWhoReactedAndNotInVC:
                users = users + "<@{0}> ".format(x)
            if users == "":
                pass
            else:
                await games.messageToPing.channel.send("{0} you're late, get in the VC!".format(users))
        else:
            pass


client.run(os.environ["BOTTOKEN"])

import asyncio
import datetime
import os
from importlib import reload

import discord
from discord.ext import commands, tasks
from discord.ext.commands.core import has_permissions, CheckFailure

import settings

client = commands.Bot(command_prefix="?", case_insensitive=True)

currentSessionGame = {}
whoReactedWithYes = []
whoReactedWithMaybe = []
sessionOwner = 0
sessionTime = datetime.datetime(datetime.datetime.now().year,
                                datetime.datetime.now().month,
                                datetime.datetime.now().day,
                                20, 0, 0) + datetime.timedelta(days=1)
foundGame = False
stopTime = datetime.datetime(datetime.datetime.now().year,
                             datetime.datetime.now().month,
                             datetime.datetime.now().day,
                             5, 0, 0) + datetime.timedelta(days=1)
tomorrow = False


def seconds_until_time(val2):
    return int((val2 - datetime.datetime.now()).total_seconds())


async def change_status(game, time, started=False, tomorrow=False):
    if started:
        await client.change_presence(status=discord.Status.dnd ,activity=discord.Game(name="{0} {1}".format(
            game,
            settings.sessionRightNowMessage
        )))
    else:
        if tomorrow:
            await client.change_presence(status=discord.Status.idle ,activity=discord.Game(name="{0} | {1} tomorrow {2}".format(
                game,
                time,
                settings.timezone
            )))
        else:
            await client.change_presence(status=discord.Status.idle ,activity=discord.Game(name="{0} | {1} {2}".format(
                game,
                time,
                settings.timezone
            )))


async def clear():
    global currentSessionGame
    global sessionTime
    global foundGame
    global whoReactedWithYes
    global whoReactedWithMaybe
    global sessionOwner
    global stopTime
    global tomorrow
    await settings.messageToPing.unpin()
    settings.messageToPing = None
    sessionOwner = 0
    whoReactedWithYes = []
    whoReactedWithMaybe = []
    foundGame = False
    tomorrow = False
    currentSessionGame = {}
    sessionTime = datetime.datetime(datetime.datetime.now().year,
                                    datetime.datetime.now().month,
                                    datetime.datetime.now().day,
                                    20, 0, 0) + datetime.timedelta(days=1)
    stopTime = datetime.datetime(datetime.datetime.now().year,
                                 datetime.datetime.now().month,
                                 datetime.datetime.now().day,
                                 5, 0, 0) + datetime.timedelta(days=1)
    await client.change_presence(activity=discord.Game(name=settings.noGameMessage))

async def can_use_command(ctx):
    if ctx.author.id not in settings.bannedUsers:
        if ctx.channel.id in settings.gameChannels:
            if not bool(currentSessionGame):
                return True
            else:
                if ctx.channel.id == currentSessionGame["channelID"]:
                    return True
                else:
                    await ctx.send("There is already a session in <#{0}>".format(currentSessionGame["channelID"]))
                    return False
        else:
            await ctx.send("This isn't a game channel!")
            return False
    else:
        await ctx.send("You have been banned from using commands!")
        return False


@client.event
async def on_ready():
    print("Bot is ready")
    change_status_at_session_start.start()
    await client.change_presence(activity=discord.Game(name=settings.noGameMessage))


@client.event
async def on_member_join(member):
    if settings.joinMessage != "":
        await member.send(settings.joinMessage)


@client.event
async def on_reaction_add(reaction, user):
    global whoReactedWithYes
    global whoReactedWithMaybe
    if bool(currentSessionGame):
        if str(reaction) == settings.emojis[0] and reaction.message.id == settings.messageToPing.id:
            if user.id == client.user.id:
                pass
            else:
                whoReactedWithYes.append(user.id)

        if str(reaction) == settings.emojis[1] and reaction.message.id == settings.messageToPing.id:
            if user.id == client.user.id:
                pass
            else:
                whoReactedWithMaybe.append(user.id)


@client.event
async def on_raw_reaction_remove(payload):
    global whoReactedWithYes
    global whoReactedWithMaybe
    if bool(currentSessionGame):
        if payload.emoji.name == settings.emojisName[0]:
            whoReactedWithYes.remove(payload.user_id)

        if payload.emoji.name == settings.emojisName[1]:
            whoReactedWithMaybe.remove(payload.user_id)


@client.command(description=settings.descriptions["updatesettings"])
@has_permissions(administrator=True)
async def updatesettings(ctx):
    if not bool(currentSessionGame):
        reload(settings)
        await ctx.send("The settings have been updated!")
    else:
        await ctx.send("When the session ends, or it might break!")
    
@updatesettings.error
async def updatesettings_error(error, ctx):
    pass

@client.command(description=settings.descriptions["hostgame"])
async def hostgame(ctx, time="20:00", *, statusMessage=""):
    if await can_use_command(ctx):
        for game in settings.gameList:
            if game["channelID"] == ctx.channel.id:
                global currentSessionGame
                global sessionOwner
                global sessionTime
                global stopTime
                global tomorrow

                currentSessionGame = game
                sessionOwner = ctx.author.id

                if not statusMessage == "":
                    tempMessage = " " + statusMessage + " "
                else:
                    tempMessage = " {0}".format(statusMessage)

                sessionTime = datetime.datetime(datetime.datetime.now().year,
                                                datetime.datetime.now().month,
                                                datetime.datetime.now().day,
                                                int(time[0:2]),
                                                int(time[3:5]), 0)
                stopTime = datetime.datetime(datetime.datetime.now().year,
                                             datetime.datetime.now().month,
                                             datetime.datetime.now().day,
                                             5, 0, 0) + datetime.timedelta(days=1)

                if int(seconds_until_time(sessionTime)) <= 0:
                    sessionTime += datetime.timedelta(days=1)
                    stopTime += datetime.timedelta(days=1)
                    await change_status(game["name"], time, False, True)
                    tomorrow = True
                else:
                    await change_status(game["name"], time, False)

                await ctx.send("<@&{0}>{1}session at {2} {3}?".format(currentSessionGame["roleID"],
                                                                      tempMessage,
                                                                      time,
                                                                      settings.timezone
                                                                      ))
                await asyncio.sleep(0.5)
                settings.messageToPing = ctx.channel.last_message
                await settings.messageToPing.pin()
                for emoji in settings.emojis:
                    await settings.messageToPing.add_reaction(emoji)
            else:
                continue


@client.command(description=settings.descriptions["endhost"])
async def endhost(ctx):
    global sessionTime
    global whoReactedWithYes
    if await can_use_command(ctx):
        if seconds_until_time(sessionTime) >= 0:
            await ctx.send("Can't end the session, it hasn't even started yet!")
        else:
            await ctx.send("Session has been ended!")
            await clear()


@client.command(description=settings.descriptions["cancelhost"])
async def cancelhost(ctx):
    global sessionOwner
    global sessionTime
    if await can_use_command(ctx):
        if ctx.author.id in [sessionOwner, 108530201708773376, 337138856858222592, 277017606446252032]:
            if seconds_until_time(sessionTime) > 0:
                users = ""
                for x in whoReactedWithYes:
                    users = users + "<@{0}>, ".format(x)
                if users == "":
                    users = "S"
                else:
                    users = users + "s"
                await ctx.send("{0}ession has been cancelled!".format(users))
                await clear()
            else:
                await ctx.send("Session is already started!\nUse `?endhost` instead!")
        else:
            await ctx.send("You can't use this command, you're not the session owner!")


@client.command(description=settings.descriptions["time"])
async def time(ctx):
    if await can_use_command(ctx):
        if bool(currentSessionGame):
            seconds = seconds_until_time(sessionTime)
            if seconds > 0:
                minutes = 0
                hours = 0
                while seconds >= 60:
                    seconds -= 60
                    minutes += 1
                while minutes >= 60:
                    minutes -= 60
                    hours += 1
                if minutes == 0:
                    await ctx.send("{0} seconds remaining until the game session!".format(seconds))
                elif hours == 0:
                    await ctx.send("{0} minutes and {1} seconds remaining until the game session!".format(
                        minutes,
                        seconds
                    ))
                else:
                    await ctx.send("{0} hours, {1} minutes and {2} seconds remaining until the game session!".format(
                        hours,
                        minutes,
                        seconds
                    ))
            else:
                await ctx.send("Session has already started!")
        else:
            await ctx.send("There is no session!")


@client.command(description=settings.descriptions["status"])
async def status(ctx):
    global whoReactedWithYes
    global whoReactedWithMaybe
    if await can_use_command(ctx):
        if bool(currentSessionGame):
            statusStats = discord.Embed(title="Status",
                                        color=0xf4adf9)
            tempReactYes = ""
            tempReactMaybe = ""
            for user in whoReactedWithYes:
                tempReactYes = tempReactYes + f"<@{user}> "

            for user in whoReactedWithMaybe:
                tempReactMaybe = tempReactMaybe + f"<@{user}> "

            if tempReactYes == "":
                tempReactYes = "Nobody"

            if tempReactMaybe == "":
                tempReactMaybe = "Nobody"

            statusStats.add_field(
                name="People who are sure {0} {1}".format(
                    settings.emojis[0], len(whoReactedWithYes)),
                value=tempReactYes,
                inline=False)

            statusStats.add_field(
                name="People who are unsure {0} {1}".format(
                    settings.emojis[1], len(whoReactedWithMaybe)),
                value=tempReactMaybe,
                inline=False)

            await ctx.send(embed=statusStats)
        else:
            await ctx.send("There is no session!")


# @client.command(description=settings.descriptions["addrole"])
# async def addrole(ctx, user: discord.Member, role: discord.Role):


# @tasks.loop(seconds=10)
@tasks.loop(minutes=5)
async def change_status_at_session_start():
    global tomorrow
    global stopTime
    if bool(currentSessionGame):
        timeToSleep = 600
        # timeToSleep = 10
        if tomorrow:
            await asyncio.sleep(seconds_until_time(datetime.datetime(datetime.datetime.now().year,
                                                                     datetime.datetime.now().month,
                                                                     datetime.datetime.now().day,
                                                                     0, 0, 0)))
            await change_status(currentSessionGame["name"], sessionTime, False, False)
        await asyncio.sleep(seconds_until_time(sessionTime) - timeToSleep)
        stopTime = datetime.datetime(datetime.datetime.now().year,
                                     datetime.datetime.now().month,
                                     datetime.datetime.now().day,
                                     5, 0, 0) + datetime.timedelta(days=1)
        await settings.messageToPing.channel.send("<@&{0}> in 10 minutes!".format(currentSessionGame["roleID"]))
        await asyncio.sleep(timeToSleep)
        if len(whoReactedWithYes) == 1:
            peopleVPerson = "is one person"
        else:
            peopleVPerson = "are {0} people".format(
                len(whoReactedWithYes))
        await settings.messageToPing.channel.send(
            "{0} session started! There {1} who reacted with {2}".format(
                currentSessionGame["name"],
                peopleVPerson,
                settings.emojis[int(0)]
            ))
        await change_status(currentSessionGame["name"], sessionTime, True)
        await asyncio.sleep(timeToSleep)
        peopleWhoReactedAndNotInVC = []
        peopleInVC = client.get_channel(
            settings.sessionVCID).voice_states.keys()
        for user in whoReactedWithYes:
            if user in peopleInVC:
                pass
            else:
                if user == client.user.id:
                    pass
                else:
                    peopleWhoReactedAndNotInVC.append(user)
        users = ""
        for x in peopleWhoReactedAndNotInVC:
            users = users + "<@{0}> ".format(x)
        if users == "":
            pass
        else:
            await settings.messageToPing.channel.send("{0}you're late, get in the VC!".format(users))
        x = seconds_until_time(stopTime)
        await asyncio.sleep(seconds_until_time(stopTime))
        await clear()

try:
    client.run(os.environ["BOTTOKEN"])
except KeyboardInterrupt:
    client.logout()
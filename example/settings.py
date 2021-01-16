AmongUs = {
    "name": "Among Us",
    "channelID": 775765356257083434,
    "roleID": 776530476566315068
}
SCP = {
    "name": "SCP: SL",
    "channelID": 768845793586053190,
    "roleID": 776530859099553832
}
GMod = {
    "name": "Garry's Mod",
    "channelID": 768844585271033888,
    "roleID": 776530820655349760
}
Minecraft = {
    "name": "Minecraft",
    "channelID": 737250225735073852,
    "roleID": 776530927702245421
}
Test = {
    "name": "Test",
    "channelID": 781207553530527774,
    "roleID": 781210527757762580
}
Generic = {
    "name": "Generic",
    "channelID": 781207580672393286,
    "roleID": 781229978137526353
}
gameList = [AmongUs, SCP, GMod, Minecraft, Test, Generic]
gameChannels = []
allRoles = [691053724826599484]
for game in gameList:
    gameChannels.append(game["channelID"])
    allRoles.append(game["roleID"])
noGameMessage = "Nothing planned yet!"
sessionRightNowMessage = "| now!"
emojis = ["<:millieHappy:776507012832952341>", "<:millieOhNo:776507015258177566>"]
emojisName = ["darkside_ok", "thonkside"]
sessionVCID = 783656335350431755
timezone = "CET"
bannedUsers = []
messageToPing = None
sessionTime = {
    "hour": 20,
    "minute": 0
}
descriptions = {
    "hostgame": f"?hostgame - Will host a session. There are multiple ways of using this command\n?hostgame - Defaults to the default time (<Role-Tag Session at 20:00 {timezone}?)\n?hostgame <time> - Defines a custom time (<Role-Tag> Session at <time> {timezone}?)\n?hostgame <time> <message> - defines a custom message (<Role-Tag> <message> at <time> {timezone}?",
    "endhost": "?endhost - Will end the session and reset the status to idle",
    "cancelhost": "?cancelhost - Will cancel the currently planned session and tag all people who reacted with the Thumb Emoji, also resets the Status to idle",
    "time": "?time - Shows you how much time is left until the session is going to start",
    "updatesettings": "**ONLY USABLE BY ADMINS**\nUpdates the settings and game list without restarting the bot",
    "addrole": "**ONLY USABLE BY ADMINS**\nAdds a role to everyone",
    "removerole": "**ONLY USABLE BY ADMINS**\nRemoves a role from everyone",
    "status": "Not to be confused with ?time, it tells how many people reacted with a yes and a maybe"
}

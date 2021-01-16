Example = {
    "name": "", 
    "channelID": 0, 
    "roleID": 0    
}
gameList = [Example]
gameChannels = []
allRoles = [691053724826599484]
for game in gameList:
    gameChannels.append(game["channelID"])
    allRoles.append(game["roleID"])
noGameMessage = ""
sessionRightNowMessage = ""
emojis = ["", ""]
emojisName = ["", ""]
sessionVCID = 0
timezone = ""
bannedUsers = []
messageToPing = None
sessionTime = {
    "hour": 0,
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

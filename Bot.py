import asyncio
from imagePull import getPic, picPull
from MAL import userClassCreator, fetchAnimeList


class Bot:

    def __init__(self, client):
        self.client = client
        self.delete = []
        self.player = None

    async def sendMessage(self, channel, message, tts=False):
        """Send a message to the channel"""

        message = await self.client.send_message(channel, message, tts=tts)

        return message

    async def sendImage(self, channel, image, filename='gelPic.jpg'):
        """Send an image message to the channel"""

        message = await self.client.send_file(channel, image,
                                              filename=filename)
        return message

    async def eroSearch(self, message, tags, n):
        """ Send n images to a discord text channel"""

        self.delete.append(message)

        images = await getPic(n, tags)

        for image in images:
            msg = await self.sendImage(message.channel, image)
            self.delete.append(msg)

        delete = await self.sendMessage(message.channel,
                                        "Deleting in 15 seconds")
        self.delete.append(delete)

        await asyncio.sleep(15)

        await self.client.delete_messages(self.delete)
        self.delete.clear()

    async def malSearch(self, channel, username):
        # Raw data pulled
        userData, animeData = fetchAnimeList(username)

        # Data is processed into mangaeable objects
        userData = userClassCreator(userData)

        nameMsg = '***' + userData.name + '***'
        await self.sendMessage(channel, nameMsg)

        # Profile Picture
        #######################################################################
        URL = ("https://myanimelist.cdn-dena.com/images/userimages/" +
               str(userData.id) + ".jpg")

        profile = await picPull(URL)
        await self.sendImage(channel, profile, filename=username + ".jpg")

        # User Information
        #######################################################################

        info = '```'

        info += '{:<30}{:•<10}{:<5}{:<10}'.format("Currently Watching", "", "",
                                                  str(userData.watching))
        info += "\n"
        info += '{:<30}{:•<10}{:<5}{:<10}'.format("Completed", "", "",
                                                  str(userData.completed))
        info += "\n"
        info += '{:<30}{:•<10}{:<5}{:<10}'.format("Dropped", "", "",
                                                  str(userData.dropped))
        info += "\n"
        info += '{:<30}{:•<10}{:<5}{:<10}'.format("Plan to Watch", "", "",
                                                  str(userData.planToWatch))
        info += "\n"
        info += '{:<30}{:•<10}{:<5}{:<10}'.format("Total Days Spent Watching",
                                                  "", "",
                                                  str(userData.daysSpent) +
                                                  " hours")
        info += '```'

        await self.sendMessage(channel, info)

    async def playAudio(self, voiceChannel, track, vol=0.75):
        # message.author.voice.voice_channel
        voice = await self.client.join_voice_channel(voiceChannel)
        player = voice.create_ffmpeg_player(track)
        player.volume = vol
        self.player = player
        player.start()
        while(player.is_playing()):
            asyncio.sleep(1)
        await voice.disconnect()

    async def changeVol(self, vol):
        try:
            self.player.volume = vol
        except ValueError:
            print('No player currently active')

    async def inspectUser(self, channel, user):
        members = self.client.get_all_members()
        target = None
        for member in members:
            if member.nick == user or member.name == user:
                target = member

        link = ''
        if target is None:
            self.delete.append(await self.sendMessage(channel, 'No user by' +
                                                      'that name in the' +
                                                      'channel'))
            await asyncio.sleep(5)
            for k in self.delete:
                await self.client.delete_message(k)

        link = target.avatar_url
        img = await picPull(link)

        await self.sendImage(channel, img, user + '.jpg')

    async def pickUser(channel):
        pass

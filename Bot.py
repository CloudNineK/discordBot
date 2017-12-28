import os
import asyncio
import discord
from imagePull import getPic, picPull
from MAL import fetchAnimeData, searchAnime, searchManga


class Bot:

    def __init__(self, client):
        self.client = client
        self.delete = []
        self.player = None

    async def send_message(self, channel, message, tts=False):
        """Send a message to the channel"""

        message = await self.client.send_message(channel, message, tts=tts)
        return message

    async def send_embed(self, channel, embed):
        """Send a message to the channel"""

        message = await self.client.send_message(channel, embed=embed)
        return message

    async def send_image(self, channel, image, filename='gelPic.jpg'):
        """Send an image to the channel"""

        message = await self.client.send_file(channel, image,
                                              filename=filename)
        return message

    async def clean(self, message, num):
        """ Deletes the last n messages sent by the bot"""

        def check(message):
            return (message.author == self.client.user or message.content[0] ==
                    '!')
        channel = message.channel
        await self.client.purge_from(channel, limit=int(num), check=check)

    async def ero_search(self, message, tags, n=3):
        """ Send n gelbooru images to a discord text channel"""

        n = int(n)
        channel = message.channel
        self.delete.append(message)

        images = await getPic(n, tags)

        for image in images:
            msg = await self.send_image(channel, image)
            self.delete.append(msg)

        notify = await self.send_message(channel, "Deleting in 10 seconds")
        self.delete.append(notify)

        await asyncio.sleep(10)

        await self.client.delete_messages(self.delete)
        self.delete.clear()

    async def mal_search(self, message, username, type):
        """ Search user's MAL profile and display stats"""

        channel = message.channel

        # Raw data pulled
        userData = fetchAnimeData(username)

        # Profile Picture
        pURL = ("https://myanimelist.cdn-dena.com/images/userimages/" +
                str(userData.id) + ".jpg")

        URL = "https://myanimelist.net/profile/" + userData.name

        tString = '***' + userData.name + "\'s Profile***"
        em = discord.Embed(title=tString, url=URL, colour=0x2E51A2)
        em.set_thumbnail(url=pURL)

        # Author
        iURL = ('https://myanimelist.cdn-dena.com/img/sp/icon/apple-touch-icon'
                '-256.png')
        sURL = 'https://myanimelist.net'
        em.set_author(name='My Anime List', url=sURL, icon_url=iURL)

        # Fields
        em.add_field(name='Currently Watching', value=str(userData.aWatching))
        em.add_field(name='Completed', value=str(userData.aCompleted))
        em.add_field(name='Dropped', value=str(userData.aDropped))
        em.add_field(name='Plan to Watch', value=str(userData.aPlanToWatch))
        em.add_field(name='Total Hours Spent Watching',
                     value=str(userData.aDaysSpent))

        await self.send_embed(channel, em)

    async def play_audio(self, message, track, vol=0.75):

        voiceChannel = message.author.voice.voice_channel

        # convert track name to path name
        track = os.cwd() + '/Audio/' + track + '.mp3'
        print(track)
        print(os.path.isfile(track))

        # Join Voice Channel
        voice = await self.client.join_voice_channel(voiceChannel)

        # Initialize audio player
        player = voice.create_ffmpeg_player(track)
        player.volume = vol
        self.player = player
        player.start()

        # Disconnect if player is not currently playing
        while(player.is_playing()):
            asyncio.sleep(1)
        await voice.disconnect()

    async def change_vol(self, message, vol):
        try:
            self.player.volume = vol
        except ValueError:
            print('No player currently active')

    async def inspect_user(self, message, user):
        channel = message.channel

        # Get target member from a list of members
        members = self.client.get_all_members()
        target = None
        for member in members:
            if member.nick == user or member.name == user:
                target = member

        # Handle user not found
        link = ''
        if target is None:
            noUsr = 'No user by that name in the channel'
            self.delete.append(await self.send_message(channel, noUsr))
            await asyncio.sleep(5)
            for k in self.delete:
                await self.client.delete_message(k)
            return

        # Send profile image (SLOW)
        link = target.avatar_url
        img = await picPull(link)
        await self.send_image(channel, img, user + '.jpg')

        # Send name and nickname(optional)
        if target.nick is None:
            uName = target.name
        else:
            uName = target.nick + ' (' + target.name + ')'
        msg = '***' + uName + '***'
        await self.send_message(channel, msg)

        # Send member roles
        roles = target.roles
        if len(roles) > 1:

            info = '```'
            info += '\nRoles:'
            roles.pop(0)
            for role in roles:
                info += '\n' + role.name

            info += '```'

            await self.send_message(channel, info)

    async def consolidate(self, message, channel_to, channel_from=None):

        channel_move_to = None
        channel_move_from = None
        channel = message.channel

        all_channels = self.client.get_all_channels()
        for channel in all_channels:
            if channel.name[2:] == channel_to:
                channel_move_from = channel

        all_channels = self.client.get_all_channels()
        for channel in all_channels:
            if channel.name[2:] == channel_from:
                print(channel.name[2:] + ' ')
                print(channel_from + '\n')
                channel_move_to = channel

        print(str(channel_move_to))
        print(str(channel_move_from))

        users = []
        for user in channel_move_from.voice_members:
            users.append(user)

        try:
            for user in users:
                await self.client.move_member(user, channel_move_to)
        except Exception:
            print('failure')

    async def ani_search(self, message, title):
        channel = message.channel
        anime = await searchAnime(title)  # Dictionary containing anime attrib

        pic = await picPull(anime['image'])
        fname = 'show.jpg'
        await self.send_image(channel, pic, filename=fname)
        await self.send_message(channel, anime['synopsis'])

    async def manga_search(self, message, title):
        channel = message.channel
        manga = await searchManga(title)  # Dictionary containing anime attrib

        pic = await picPull(manga['image'])
        fname = 'show.jpg'
        await self.send_image(channel, pic, filename=fname)
        await self.send_message(channel, manga['synopsis'])

    async def list_users(self, message, arg="role"):
        """ List user in the channel"""
        channel = message.channel
        server = channel.server

        members = server.members
        members = [member for member in members if str(member.status) !=
                   'offline' and member.bot is not True]
        members = sorted(members, key=lambda x: x.nick if x.nick == str else
                         str(x))

        message = ''

        if arg == 'role':
            for member in members:
                name = member.nick if type(member.nick) == str else str(member)

                pos = name.find('#')

                if pos != -1:
                    name = name[:pos]

                message += '**' + name + '**' + '\n'

        if arg == 'game':
            members = [member for member in members if member.game is not None]
            members = sorted(members, key=lambda x: str(x.game))

            for member in members:
                name = member.nick if type(member.nick) == str else str(member)
                game = str(member.game)

                pos = name.find('#')

                if pos != -1:
                    name = name[:pos]

                message += ('**' + game + '**' + ': ' + '__' + name + '__' +
                            '\n')

        if arg == 'emoji':
            emojis = server.emojis
            for emoji in emojis:
                message += ('<a:' + emoji.name + ':' + emoji.id + '> ' +
                            ':' + emoji.name + ':\n')

        await self.send_message(channel, message)

        pass

    async def error_message(self, channel):
        title = 'Error'
        description = 'Sorry, something went wrong'
        colour = 0xff6961
        em = discord.Embed(title=title, description=description, colour=colour)
        self.send_embed(channel, em)
        pass

    async def test(self, message):
        m = '\\:pepe:'
        await self.send_message(message.channel, m)
        pass

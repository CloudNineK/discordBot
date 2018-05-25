import asyncio
import discord

from datetime import datetime
from imagePull import getPic, picPull
from MAL import fetchAnimeData, searchAnime, searchManga
from random import choice

# External modules
from markov import Markov

# TODO: !age in days


class Bot:

    def __init__(self, client):
        self.client = client
        self.delete = []
        self.player = None
        self.markov = Markov('discord.txt')

        # List of error images
        with open('errPics.txt', 'r') as f:
            self.errorPics = f.read().splitlines()

        # List of welcome images
        with open('welcPics.txt', 'r') as f:
            self.welcPics = f.read().splitlines()

    async def clean(self, message, num=5):
        """ Deletes the last n messages sent by the bot"""
        channel = message.channel

        num = int(num)
        num += 1

        def check(message):
            def check_exc(message):
                try:
                    return message.content[0] == '!'
                except IndexError:
                    return False

            return (message.author == self.client.user or check_exc(message))
        await channel.purge(limit=num, check=check)

    async def ero_search(self, message, tags, t=10, n=3):
        """ Send n gelbooru images to a discord text channel"""

        n = int(n)
        delete = []
        channel = message.channel

        try:
            images = await getPic(n, tags)
        except ValueError:
            errorTitle = "Invalid Tags"
            errorDescription = "Sorry, no images were found."
            await self.error(channel, errorTitle, errorDescription)
            await asyncio.sleep(10)
            await message.delete()
            return

        files = []
        for image in images:
            # Yea...
            files.append(discord.File(image, str(image) + '.png'))

        pics = await channel.send(files=files)

        notify = await channel.send("Deleting in " + str(t) + " seconds")
        delete.append(notify)
        delete.append(pics)
        delete.append(message)

        await asyncio.sleep(int(t))

        await channel.delete_messages(delete)

    async def mal_search(self, message, username):
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

        # Fields
        em.add_field(name='Currently Watching', value=str(userData.aWatching))
        em.add_field(name='Completed', value=str(userData.aCompleted))
        em.add_field(name='Dropped', value=str(userData.aDropped))
        em.add_field(name='Plan to Watch', value=str(userData.aPlanToWatch))
        em.add_field(name='Total Hours Spent Watching',
                     value=str(userData.aDaysSpent))

        # Author
        iURL = ('https://myanimelist.cdn-dena.com/img/sp/icon/apple-touch-icon'
                '-256.png')
        sURL = 'https://myanimelist.net'
        em.set_author(name='My Anime List', url=sURL, icon_url=iURL)

        await channel.send(embed=em)

    async def inspect_user(self, message, user):
        channel = message.channel

        # Get target member from a list of members
        # TODO: discord.utils.find()
        members = channel.guild.members
        target = None
        for member in members:
            if member.nick == user or member.name == user:
                target = member

        # TODO: handle this with the error method
        if target is None:
            err = 'No user by that name in the channel'
            delete = [await self.error(channel, err)]
            await asyncio.sleep(5)
            await channel.delete(delete)
            return

        # Username
        if target.nick is None:
            uName = target.name
        else:
            uName = target.nick + ' (' + target.name + ')'

        em = discord.Embed(title=uName, url=target.avatar_url,
                           colour=target.color.value)
        em.set_thumbnail(url=channel.guild.icon_url)
        print(channel.guild.icon_url)

        joined = datetime.now() - target.joined_at
        em.add_field(name='Role', value=str(target.top_role))
        em.add_field(name='Age', value=(str(joined.days) + ' days'))
        em.set_image(url=target.avatar_url)

        await channel.send(embed=em)

    async def voice_move(self, message, channel_to, channel_from=None):

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
        manga = await searchManga(title)

        # embed
        url = 'https://myanimelist.net/manga/' + manga.dbid
        em = discord.Embed(title=manga.title, url=url, colour=0x2E51A2)
        em.set_thumbnail(url=manga.image)

        # Fields
        em.add_field(name='Synopsis', value=str(manga.synopsis))

        # Author
        iURL = ('https://myanimelist.cdn-dena.com/img/sp/icon/apple-touch-icon'
                '-256.png')
        sURL = 'https://myanimelist.net'
        em.set_author(name='My Anime List', url=sURL, icon_url=iURL)

        await channel.send(embed=em)

    async def list_users(self, message, arg="role"):
        """ List user in the channel"""

        # TODO: embed everything

        channel = message.channel
        guild = message.guild

        members = guild.members
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
            # TODO: "is not none", handle no users playing game
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

                if message == '':
                        message = ('No users in the server are currently'
                                   'playing games')

        if arg == 'emoji':
            emojis = guild.emojis
            for emoji in emojis:
                message += (str(emoji) + ' :' + emoji.name + ':\n')

        await channel.send(message)

        pass

    async def error(self, channel, title, description):
        colour = 0xff6961

        em = discord.Embed(title=title, description=description, colour=colour)
        em.set_thumbnail(url=choice(self.errorPics))
        err = await channel.send(embed=em)

        await asyncio.sleep(10)
        await err.delete()

    async def welcome(self, channel, username):
        colour = 0xaec6cf
        title = "Welcome!"
        description = "Welcome to the server " + username

        em = discord.Embed(title=title, description=description, colour=colour)
        em.set_thumbnail(url=choice(self.welcPics))
        await channel.send(embed=em)

    async def help(self, channel, message):
        pass

    async def markov_gen(self, message):
        channel = message.channel
        await channel.send(self.markov.generate())

    async def test(self, message):
        m = '\\:pepe:'
        await self.send_message(message.channel, m)
        pass

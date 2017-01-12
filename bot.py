import discord
import asyncio

# EROSEARCH
from getDataETree import getPic

# MAL LOOKUP
from userClass import userClassCreator
from getDataETree import picPull
from getDataETreeMAL import fetchAnimeList

# AUDIO
import os

client = discord.Client()
discord.opus.load_opus('/usr/lib/x86_64-linux-gnu/libopus.so.0')

# Come back to this
gelTags = []
with open('gelTags.txt', 'r') as f:
    for line in f:
        gelTags.append(line.strip())
gelSet = set(gelTags)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('-------------')


@client.event
async def on_message(message):

    # EROSEARCH
    if message.content.startswith('!eroSearch'):
        delete = []  # list of messages to delete
        delete.append(message)

        start = message.content.find(" ") + 1

        query = message.content[start:]

        await client.send_typing(message.channel)

        delete.append(await client.send_message(message.channel, 'Searching',
                                                tts=False))
        delete.extend(await eroFunc(message, query))

        await asyncio.sleep(15)
        for k in delete:
            await client.delete_message(k)

    # EROSAFE
    if message.content.startswith('!eroSafe'):
        delete = []  # list of messages to delete
        delete.append(message)

        start = message.content.find(" ") + 1

        query = message.content[start:]
        query = query.split('+')

        await client.send_typing(message.channel)

        delete.append(await client.send_message(message.channel, 'Searching',
                                                tts=False))
        delete.extend(await eroSafe(message, query))

        await asyncio.sleep(15)
        for k in delete:
            await client.delete_message(k)

    # MAL LOOKUP
    if message.content.startswith('!MAL'):
        start = message.content.find(" ") + 1

        user = message.content[start:]

        await MAL_Info(message, user)

    # AUDIO
    if message.content.startswith('!voice'):
        if message.author.nick == 'Terrence':  # User specific

            start = message.content.find(" ") + 1
            query = message.content[start:]

            await audio(message, os.getcwd() + '/Audio/' + query + '.mp3')


async def eroFunc(message, tags):
    site = 'http://gelbooru.com'
    delete = []

    images = await getPic(3, site, tags)

    for image in images:
        x = await client.send_file(message.channel,
                                   image,
                                   filename="x.jpg")
        delete.append(x)

    deleteNotif = "Deleting in 15 seconds"

    n = await client.send_message(message.channel, deleteNotif, tts=False)
    delete.append(n)

    return delete


async def eroSafe(message, tags):
    site = 'http://gelbooru.com'
    delete = []

    tagStr = ''
    for ktag in tags:
        tagStr += ktag + ' + '
        if ktag not in gelSet:
            print(ktag + ' not found')
            return

    tagStr = tagStr[:len(tagStr) - 3]
    print(tags)
    images = await getPic(3, site, tagStr)

    for image in images:
        x = await client.send_file(message.channel,
                                   image,
                                   filename="x.jpg")
        delete.append(x)

    # put this in main function
    deleteNotif = "Deleting in 15 seconds"

    n = await client.send_message(message.channel, deleteNotif, tts=False)
    delete.append(n)

    return delete


async def MAL_Info(message, user):

    # Raw data pulled
    userData, animeData = fetchAnimeList(user)
    # Data is processed into mangaeable objects
    userData = userClassCreator(userData)

    nameMsg = '***' + userData.name + '***'
    await client.send_message(message.channel, nameMsg, tts=False)

    # Profile Picture
    ###########################################################################
    URL = ("https://myanimelist.cdn-dena.com/images/userimages/" +
           str(userData.id) + ".jpg")

    profile = await picPull(URL)
    await client.send_file(message.channel,
                           profile,
                           filename=user + ".jpg")

    # User Information
    ###########################################################################

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
    info += '{:<30}{:•<10}{:<5}{:<10}'.format("Total Days Spent Watching", "",
                                              "", str(userData.daysSpent) +
                                              " hours")
    info += '```'

    await client.send_message(message.channel, info, tts=False)


async def audio(message, track):
    voice = await client.join_voice_channel(message.author.voice.voice_channel)
    player = voice.create_ffmpeg_player(track)
    player.volume = 0.75
    player.start()
    while(player.is_playing()):
        asyncio.sleep(1)
    print('ya')
    await voice.disconnect()


client.run('MjMyMzQ3Mzg5MjY3MTQ4ODAw.CutEGg.Tgtv8cC1sQiiFtMttFYL1PO83io')

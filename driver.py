import discord
import asyncio
from Bot import Bot

client = discord.Client()
discord.opus.load_opus('/usr/lib/x86_64-linux-gnu/libopus.so.0')

bot = Bot(client)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('-------------')


@client.event
async def on_message(message):

    if message.content.startswith('Meido,'):

        start = message.content.find(' ') + 1
        query = message.content[start:message.content.find(' ', start)]
        args  = message.content[start + len(query) + 1:]

        await client.send_typing(message.channel)

        if query == 'eroSearch':
            await bot.eroSearch(message.channel, args, 3)

        if query == 'MALsearch':
            await bot.malSearch(message.channel, args)

        if query == 'inspect':
            await bot.inspectUser(message.channel, args)

        if query == 'play':
            await bot.playAudio(message.author.voice.voice_channel, args)

        if query == 'changeVol':
            await bot.changeVol(args)

        if query == 'pick':
            pass


client.run('MjMyMzQ3Mzg5MjY3MTQ4ODAw.CutEGg.Tgtv8cC1sQiiFtMttFYL1PO83io')

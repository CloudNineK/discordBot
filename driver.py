#!/usr/lib/python3.6

import discord
from Bot import Bot

client = discord.Client()
# discord.opus.load_opus('/usr/lib/libopus.so')
bot = Bot(client)


# Unwrap list of args
async def wrapper(func, args):
    if len(args) > 0:
        await func(*args)
    else:
        await func()


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('-------------')


@client.event
async def on_message(message):

    if message.content.startswith('!'):

        query = (message.content + ' ')[1:message.content.find(' ')]
        args = message.content[len(query) + 1:]
        args = args.split()
        args.insert(0, message)

        funcs = {'clean': bot.clean,
                 'inspect': bot.inspect_user,
                 'list': bot.list_users,
                 'ero': bot.ero_search,
                 'mal': bot.mal_search,
                 'inspect': bot.inspect_user,
                 'anime': bot.ani_search,
                 'manga': bot.manga_search,
                 'consolidate': bot.consolidate,
                 'test': bot.test}

        # Trivial to make this output error to console without stopping
        # execution
        """
        try:
            await wrapper(funcs[query], args)
        except Exception as e:
            print("Failure " + query + " " + str(args))
        """

        await wrapper(funcs[query], args)


client.run('Mjk5MjIyMjEyMzYyMjQwMDAx.C8axlw.RvgOLYv17_LNEjZlPl8lbLAK2g8')

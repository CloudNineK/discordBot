#!/usr/bin/env python3

import asyncio
import discord
import db
from discord.ext import commands

from imagePull import getPic
from MAL import fetchAnimeData
from random import choice
import datetime


# Get login token
f = open('token.txt', 'r')
t = f.read()
t = t.strip()
f.close()

# List of error images
with open('errPics.txt', 'r') as f:
    errorPics = f.read().splitlines()

# List of welcome images
with open('welcPics.txt', 'r') as f:
    welcPics = f.read().splitlines()

bot = commands.Bot(command_prefix='!')


async def error(channel, title, description):
    colour = 0xff6961

    em = discord.Embed(title=title, description=description, colour=colour)
    em.set_thumbnail(url=choice(errorPics))
    err = await channel.send(embed=em)

    await asyncio.sleep(10)
    await err.delete()


async def cTime():
    """ Return formatted system time"""

    ts = datetime.datetime.now()

    half = 'AM' if (int(ts.strftime('%H')) < 12) else 'PM'

    fts = ts.strftime("%A %b, %y at %H:%M")
    fts += half

    return fts


async def footer_stamp():

    return '© ' + bot.user.name + ' | ' + await cTime()


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('-------------')


@bot.command()
async def clean(ctx, n=5):
    """ Deletes the last n invocations and responses associated with the bot"""
    num = int(n)
    num += 1  # account for the invoking message

    def check(message):
        def check_exc(message):
            try:
                return message.content[0] == '!'
            except IndexError:
                return False

        return (message.author == ctx.bot.user or check_exc(message))
    await ctx.message.channel.purge(limit=num, check=check)


@bot.command()
async def inspect(ctx, *name):
    ''' '''

    target = None
    user = ' '.join(name)
    members = ctx.guild.members

    # Get member via user or nick name
    for member in members:
        if user.lower() in (member.display_name.lower(), member.name.lower()):
            target = member

    # If target is not found return error; break
    if target is None:
        errorTitle = "Invalid User"
        errorDescription = "Sorry, no user was found by that name"
        await error(ctx.message.channel, errorTitle, errorDescription)
        await asyncio.sleep(10)
        await ctx.message.delete()
        return

    # Display nick + user name if found
    if target.nick is None:
        uName = target.name
    else:
        uName = (target.nick + " (" + target.name + "#" + target.discriminator
                 + ")")

    # Setup embed
    em = discord.Embed(title=uName, url=target.avatar_url,
                       colour=target.color.value)

    # Discord Join Date Field
    em.add_field(name='Discord Join Date',
                 value=target.created_at.strftime('%B %d, %Y'),
                 inline=False)

    # Highest Role
    em.add_field(name='Role',
                 value=target.top_role.name,
                 inline=False)

    em.set_thumbnail(url=target.avatar_url)
    em.set_footer(text=await footer_stamp())

    # Game Roles
    roles = ctx.guild.roles
    roles.sort()

    # Get indices of game role separators
    dexes = []
    for k in range(len(roles)):
        if roles[k].name == '-----------':
            dexes.append(k)

    games = ''
    if len(dexes) is 2:
        for k in range(dexes[0] + 1, dexes[1]):
            games += roles[k].name + '\n'

    if games == '':
        games = 'None'

    em.add_field(name='Games',
                 value=games,
                 inline=False)

    await ctx.send(embed=em)

    return


@bot.command()
async def ero(ctx, *tags):
    """ Post images from gelbooru based on tags"""

    n = 5  # Number of images
    t = 20  # Time before image deletion

    try:
        images = await getPic(n, ' + '.join(tags))
    except ValueError:
        errorTitle = "Invalid Tags"
        errorDescription = "Sorry, no images were found."
        await error(ctx, errorTitle, errorDescription)
        await asyncio.sleep(10)
        await ctx.message.delete()
        return

    files = []
    delete = []
    for image in images:
        # Yea...
        files.append(discord.File(image, str(image) + '.png'))

    pics = await ctx.send(files=files)

    notify = await ctx.send("Deleting in " + str(t) + " seconds")
    delete.append(notify)
    delete.append(pics)
    delete.append(ctx.message)

    await asyncio.sleep(int(t))

    await ctx.message.channel.delete_messages(delete)


@bot.command()
async def mal(ctx, uName):
    """ Search user's MAL profile and display stats"""

    # Raw data pulled
    userData = fetchAnimeData(uName)

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

    await ctx.send(embed=em)


@bot.command()
async def echo(ctx, arg):
    await ctx.send(arg)


@bot.command()
async def whose(ctx, arg):
    pass


@bot.command()
async def irl(ctx, mode, *args):
    users = await db.tableGet('Members')

    # Setup embed
    em = discord.Embed(title='Users')

    for user in users:
        em.add_field(name=user,
                     value=users[user],
                     inline=False)

    await ctx.send(embed=em)


@bot.command()
async def test(ctx):
    roles = ctx.guild.roles
    roles.sort()
    dexes = []
    for k in range(len(roles)):
        print(roles[k])
        if roles[k].name == '-----------':
            dexes.append(k)

    print(dexes)

bot.run(t)

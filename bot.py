import discord
import asyncio
import random
from getDataETree import getPic, fetchHList

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    if message.content.startswith('!eroSearch'):
        await client.send_message(message.channel, "What tags?", tts=False)
        msg = await client.wait_for_message(author=message.author)
        tags = msg.content
        images = await getPic(3, tags)

        for image in images:
            await client.send_file(message.channel, image, filename="x.jpg")


client.run('MjMyMzQ3Mzg5MjY3MTQ4ODAw.CtYyYA.41yI5yzQ8zpzns-9FS8ueuoYW4k')

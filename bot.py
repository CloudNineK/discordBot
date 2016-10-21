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

        if (len(images) == 0):
            await client.send_message(message.channel, "Bad tag", tts=False)
            return

        delete = []
        for image in images:
            x = await client.send_file(message.channel, image, filename="x.jpg")
            delete.append(x)

        deleteNotif = "Deleting in 30 seconds"
        n = await client.send_message(message.channel, deleteNotif, tts=False)
        delete.append(n)

        await asyncio.sleep(30)
        for k in delete:
            await client.delete_message(k)
            print ("deleted")

client.run('MjMyMzQ3Mzg5MjY3MTQ4ODAw.CutEGg.Tgtv8cC1sQiiFtMttFYL1PO83io')

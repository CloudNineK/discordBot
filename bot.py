import discord
import asyncio
from getDataETree import getPic

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
        site = 'http://gelbooru.com'
        start = message.content.find(" ") + 1
        tags = message.content[start:]
        images = await getPic(3, site, tags)

        if (len(images) == 0):
            x = await client.send_message(message.channel,
                                          "Bad tag",
                                          tts=False)
            print(tags)
            await client.delete_message(message)
            await client.delete_message(x)
            return

        delete = []  # list of messages to delete
        delete.append(message)

        for image in images:
            x = await client.send_file(message.channel,
                                       image,
                                       filename="x.jpg")
            delete.append(x)

        deleteNotif = "Deleting in 30 seconds"
        n = await client.send_message(message.channel, deleteNotif, tts=False)
        delete.append(n)

        await asyncio.sleep(30)
        for k in delete:
            await client.delete_message(k)

client.run('MjMyMzQ3Mzg5MjY3MTQ4ODAw.CutEGg.Tgtv8cC1sQiiFtMttFYL1PO83io')

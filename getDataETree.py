""" Returns image object from gelbooru based on tags"""

import requests
import xml.etree.ElementTree as ET
import urllib.request as urllib
import io
import aiohttp
import asyncio
from PIL import Image
from random import randint


@asyncio.coroutine
async def fetchHList(tags):
    """ returns a list of Dictionaries containing image information
        tags is a string with format: "tag1" or "tag1 + tag2"
    """

    url = ('http://gelbooru.com/index.php?page=dapi&s=post&q=index' + '&tags=' +
           tags)

    # Request XML tree containing images based on tag
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as r:

            # Convert xml formatted data to elementree object
            root = ET.fromstring(await r.text())

            # create a list of database entries
            entries= []  # entries is a list of dictionaries
            for ent in root.iter('posts'):
                # add a dictionary of data for a single image to the entries list
                for attrib in ent:
                    entries.append(attrib.attrib)

            return entries

@asyncio.coroutine
async def getPic(rep, tags='paizuri'):
    """ returns a number of random image objects from a dictionary of image URLs
        entries is a list of dictionaries containing image information
        rep is the number of images to return

        rep is included to prevent duplicate images from being sent; if getPic
        were called 3 times with rep 0 to send 3 images with the same tag the
        chance of duplicate is much higher.
    """

    entries = await fetchHList(tags)
    images = []

    # if empty return empty array
    if (len(entries) == 0):
        return images

    # if # of entries is less than rep; rep = # of entries
    if (len(entries) < rep):
        rep = len(entries)

    ran = range(rep)

    for k in ran:
        num = randint(0, len(ran))
        fileUrl = entries[num]["file_url"]
        entries.pop(num)  # prevent duplicate images
        images.append(await picPull(fileUrl))

    return images


@asyncio.coroutine
async def picPull(url):
    """ returns image object from url"""

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as r:
            # image = urllib.urlopen(url).read()
            image = await r.read()
            imgData = io.BytesIO(image)

            return imgData

if __name__ == "__main__":
    print (fetchHList())
    print (getPic(fetchHList()))

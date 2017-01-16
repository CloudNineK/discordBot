""" Returns image object from gelbooru based on tags"""

import xml.etree.ElementTree as ET
import io
import aiohttp
from random import randint


async def fetchHList(tags):
    """ returns a list of Dictionaries containing image information
        tags is a string with format: "tag1" or "tag1 + tag2"
    """

    url = ('http://gelbooru.com/index.php?page=dapi&s=post&q=index&limit=99' +
           '&tags=' + tags)

    # Request XML tree containing images based on tag
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as r:

            # Convert xml formatted data to elementree object
            root = ET.fromstring(await r.text())

            # create a list of database entries
            entries = []  # entries is a list of dictionaries
            for ent in root.iter('posts'):
                # add a dictionary of data for a single image to the entries
                # list
                for attrib in ent:
                    entries.append(attrib.attrib)

            return entries

async def picPull(url):
    """ returns image object from url"""

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as r:
            # image = urllib.urlopen(url).read()
            image = await r.read()
            imgData = io.BytesIO(image)

            return imgData

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

    # Raise exception if no images are found for tag combination
    if (len(entries) == 0):
        raise ValueError('Tags did not yield any results')

    # if # of entries is less than rep; rep = # of entries
    if (len(entries) < rep):
        rep = len(entries)

    for k in range(rep):
        num = randint(0, (len(entries) - 1))
        fileUrl = entries[num]["file_url"]
        entries.pop(num)  # prevent duplicate images
        images.append(await picPull(fileUrl))

    return images

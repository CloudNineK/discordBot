""" This module returns information from a user's MyAnimeList account"""

import requests
from theAnimeClass import Anime

def fetchAnimeList():
    """ returns a list of anime objects for a specified user's animelist"""


    url = ('http://myanimelist.net/malappinfo.php?u=cloudninek&status=all&type'
        '=anime')

    # encode otherwise string conversion throws errors
    animelist = r.text.encode("utf-8")
    animelist = str(animelist)

    # Data from MAL is returned as an XML file.
    # It may be possible to use xml element tree to easily access this data
    # for future reference see:
    # https://docs.python.org/2/library/xml.etree.elementtree.html

    # list of xml end tags to clean up anime list in xml format
    removeList = ['</anime>', '</series_animedb_id>', '</series_title>',
                '</series_synonyms>', '</series_type>', '</series_episodes>',
                '</series_status>', '</series_start>', '</series_end>',
                '</series_image>', '</my_id>', '</my_watched_episodes>',
                '</my_start_date>', '</my_finish_date>', '</my_score>',
                '</my_status>', '</my_rewatching>', '</my_rewatching_ep>',
                '</my_last_updated>', '</my_tags>']

    # replaces tags from removelist in animelist with ',' for future splitting
    for item in removeList:
        animelist = animelist.replace(item, '')

    # major split since information for each anime is divided by an anime tag
    aList = animelist.split('<anime>')

    # create a lists consisting of the open tags to the end tags in removeList
    # e.g </series_type> becomes <series_type>
    removeListOpen = []
    for item in removeList:
        itemcut = item[:1] + item[2:]
        removeListOpen.append(itemcut)

    # replaces tags from removeListOpen in aList with ',' for future splitting
    for k in range(len(aList)):
        for split in removeListOpen:
            aList[k] = aList[k].replace(split, ',')

    # pop out the first index of aList which houses uer information
    tempval = aList.pop(0)  # holds user values not anime values

    AnimeList = []  # list of anime objects
    for item in aList:
        anilist = item.split(',')
        anilist.pop(0)
        aniObj = Anime(anilist)
        AnimeList.append(aniObj)

    return AnimeList

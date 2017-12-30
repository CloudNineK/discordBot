import requests
import aiohttp
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup as bs

""" This module processes XML information from a user's MyAnimeList account"""

# TODO: Probably a good idea to use dictionaries to initialize the classes
#       instead of lists

# Yummy hard coded credentials for search api
user = "TessBot"
pw = "SupersonicRefraction!"


# 2 classes due to MAL's request limit
class UserAnime():
    """ MAL User information; <myinfo>"""

    def __init__(self, L):
        """ L: a list of attributes respective of the <myinfo> xml tags"""

        self.id = L[0]
        self.name = L[1]

        # Anime
        self.aWatching = L[2]
        self.aCompleted = L[3]
        self.aOnhold = L[4]
        self.aDropped = L[5]
        self.aPlanToWatch = L[6]
        self.aDaysSpent = L[7]


class UserManga():
    """ MAL User information; <myinfo>"""

    def __init__(self, L):
        """ L: a list of attributes respective of the <myinfo> xml tags"""

        self.id = L[0]
        self.name = L[1]

        # Manga
        self.mReading = L[2]
        self.mCompleted = L[3]
        self.mOnhold = L[4]
        self.mDropped = L[5]
        self.mPlanToRead = L[6]
        self.mDaysSpent = L[7]


class Anime():
    """ MAL Anime information; <anime>"""

    def __init__(self, L):
        """ L: a list of attributes respective of the <anime> xml tags"""

        self.dbid = L[0]
        self.title = L[1]
        self.synonyms = L[2]
        self.typenum = L[3]
        self.episodes = L[4]
        self.status = L[5]
        self.startDate = L[6]
        self.endDate = L[7]
        self.image = L[8]
        self.myID = L[9]
        self.myWatchedEpisodes = L[10]
        self.myStartDate = L[11]
        self.myFinishDate = L[12]
        self.myScore = L[13]
        self.myStatus = L[14]
        self.myRewatching = L[15]
        self.myLastUpdated = L[16]


class AnimeSearch():
    """ MAL Anime search response information; <entry>"""

    def __init__(self, L):
        """ L: a list of attributes respective of the <anime><entry> tags"""
        self.dbid = L[0]
        self.title = L[1]
        self.english = L[2]
        self.synonyms = L[3]
        self.episodes = L[4]
        self.score = L[5]
        self.dbtype = L[6]
        self.status = L[7]
        self.startDate = L[8]
        self.endDate = L[9]
        self.synopsis = L[10]
        self.image = L[11]


class MangaSearch():
    """ MAL Manga search response information; <entry>"""

    def __init__(self, L):
        """ L: a list of attributes respective of the <manga><entry> tags"""
        self.dbid = L[0]
        self.title = L[1]
        self.english = L[2]
        self.synonyms = L[3]
        self.chapters = L[4]
        self.volumes = L[5]
        self.score = L[6]
        self.dbtype = L[7]
        self.status = L[8]
        self.startDate = L[9]
        self.endDate = L[10]
        self.synopsis = L[11]
        self.image = L[12]


def animeClassCreator(aniData):
    """ Takes a list of raw anime data and creates Anime objects"""

    # List storing anime objects for given user
    animeList = []

    for data in aniData:
        tempClass = Anime(data)
        animeList.append(tempClass)

    return animeList


def fetchAnimeList(user='cloudninek'):
    """ returns a list of anime objects for a specified user's animelist

        PreC: user must be a str
    """

    url = ('http://myanimelist.net/malappinfo.php?u=' + user +
           '&status=all&type=anime')

    # Request user data from MAL
    # Convert xml formatted data to elementree object
    r = requests.get(url)
    root = ET.fromstring(r.content)

    # create a list of anime data
    animeData = []  # animeData is a list of lists
    for anime in root.iter('anime'):
        # add a list of data for a single anime to the animeData list
        tempList = []
        for attrib in anime:
            tempList.append(attrib.text)
        animeData.append(tempList)

    return animeData


def fetchAnimeData(user='cloudninek'):
    userData = []

    aUrl = ('http://myanimelist.net/malappinfo.php?u=' + user +
            '&status=all&type=anime')

    # Request anime data from MAL
    # Convert xml formatted data to elementree object
    r = requests.get(aUrl)
    root = ET.fromstring(r.content)

    # append anime data
    for Data in root.iter('myinfo'):
        for stat in Data:
            userData.append(stat.text)

    return UserAnime(userData)


def fetchMangaData(user='cloudninek'):
    userData = []

    mUrl = ('http://myanimelist.net/malappinfo.php?u=' + user +
            '&status=all&type=manga')

    # Request manga data from MAL
    # Convert xml formatted data to elementree object
    r = requests.get(mUrl)
    root = ET.fromstring(r.content)

    # append manga data
    for Data in root.iter('myinfo'):
        for stat in Data:
            userData.append(stat.text)

    return UserManga(userData)


async def searchAnime(name):
    """ Returns a dictionary containing attributes for the searched anime"""

    basicAuth = aiohttp.BasicAuth('CloudNineK', 'Iridescenc3')

    url = "https://myanimelist.net/api/anime/search.xml?q=" + name
    async with aiohttp.ClientSession() as session:
        async with session.request('GET', url, auth=basicAuth) as r:

            anime = {}
            root = ET.fromstring(await r.text())
            for item in root[0]:
                try:
                    # Convert html encoding
                    anime[item.tag] = bs(item.text)
                    # Remove break tags
                    for e in anime[item.tag].findAll('br'):
                        e.extract()
                    anime[item.tag] = str(anime[item.tag])

                except Exception:
                    anime[item.tag] = ""

    return anime


async def searchManga(name):
    """ Returns a dictionary containing attributes for the searched manga"""

    basicAuth = aiohttp.BasicAuth('CloudNineK', 'Iridescenc3')

    url = "https://myanimelist.net/api/manga/search.xml?q=" + name
    async with aiohttp.ClientSession() as session:
        async with session.request('GET', url, auth=basicAuth) as r:

            manga = []
            root = ET.fromstring(await r.text())
            for item in root[0]:
                try:
                    # Convert html encoding
                    txt = bs(item.text)
                    # Remove break tags
                    for e in txt.findAll('br'):
                        e.extract()
                    manga.append(str(txt))

                except Exception:
                    manga.append("")

    return MangaSearch(manga)

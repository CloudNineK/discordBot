import requests
import xml.etree.ElementTree as ET

""" This module processes information from a user's MyAnimeList account"""

class User():
    """ Attributes"""

    def __init__(self, L):
        # some naming inconsistency in order to match xml roots

        # Implement easier way to do this
        self.id = L[0]
        self.name = L[1]
        self.watching = L[2]
        self.completed = L[3]
        self.onhold = L[4]
        self.dropped = L[5]
        self.planToWatch = L[6]
        self.daysSpent = L[7]

        attribList = [self.id, self.name, self.watching, self.completed,
                      self.onhold, self.dropped, self.planToWatch,
                      self.daysSpent]

        for k in range(len(attribList)):
            attribList[k] = L[k]

class Anime():
    """ Attributes"""

    def __init__(self, L):

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


# This function exists for consistency with the anime class
# While anime data is contained by a list of lists user data is contained by a
# single list and thus is trivial to intialize
def userClassCreator(userData):
    """ Takes a list of raw user data and creates user objects"""

    tempClass = User(userData)

    return tempClass

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

    # create a list of user data
    userData = []
    for Data in root.iter('myinfo'):
        for stat in Data:
            userData.append(stat.text)

    # create a list of anime data
    animeData = []  # animeData is a list of lists
    for anime in root.iter('anime'):
        # add a list of data for a single anime to the animeData list
        tempList = []
        for attrib in anime:
            tempList.append(attrib.text)
        animeData.append(tempList)

    return userData, animeData

""" Anime Object"""


class Anime(object):
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


def animeClassCreator(aniData):
    """ Takes a list of raw anime data and creates Anime objects"""

    # List storing anime objects for given user
    animeList = []

    for data in aniData:
        tempClass = Anime(data)
        animeList.append(tempClass)

    return animeList

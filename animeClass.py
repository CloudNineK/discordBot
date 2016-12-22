""" Anime Object"""


class Anime(object):
    """ Attributes"""

    def __init__(self, L):

        attribList = [self.dbid, self.title, self.synonyms, self.typenum,
                      self.episodes, self.status, self.startDate,
                      self.endDate, self.image, self.myID,
                      self.myWatchedEpisodes, self.myStartDate,
                      self.myFinishDate, self.myScore, self.myStatus,
                      self.myRewatching, self.myLastUpdated]

        for k in range(attribList):
            attribList[k] = L[k]

class AnimeLog(object):
    """ Attributes"""

    def __init__(self, List):

        temp = []
        for k in range(len(List)):
            temp.append(Anime(List[k]))

        self.list = temp

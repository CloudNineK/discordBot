""" User Object"""


class User(object):
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


# This function exists for consistency with the anime class
# While anime data is contained by a list of lists user data is contained by a
# single list and thus is trivial to intialize
def userClassCreator(userData):
    """ Takes a list of raw user data and creates user objects"""

    tempClass = User(userData)

    return tempClass

""" This module returns information from a user's MyAnimeList account"""

import requests
import xml.etree.ElementTree as ET


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

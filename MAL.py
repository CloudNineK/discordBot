""" """

from userClass import userClassCreator
from theAnimeClass import animeClassCreator
from getDataETree import fetchAnimeList


async def MAL_Info(message, user):
    user1 = raw_input('Enter your MAL account name ')
    user2 = raw_input('Enter your friend\'s MAL account name ')

    # Raw data pulled and stored for each user as LISTS
    user1_userData, user1_animeData = fetchAnimeList(user1)
    user2_userData, user2_animeData = fetchAnimeList(user2)

    # User and Animelog classes are created to store user and animelist data
    # for each user
    user1_Data = userClassCreator(user1_userData)
    user1_List = animeClassCreator(user1_animeData)

    user2_Data = userClassCreator(user2_userData)
    user2_List = animeClassCreator(user2_animeData)

    count = 0
    for item1 in user1_List:
        for item2 in user2_List:
            if item1.title == item2.title:
                count += 1
                print item1.title
    print "\nYou and %s have %d titles in common" % (user2, count)

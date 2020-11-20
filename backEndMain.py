# -*- coding: utf-8 -*-

# Sample Python code for youtube.channels.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

import os
import datetime
import googleapiclient.discovery
import config
import typing
import database
from CreatorAndVideoObjects import Creator, Video


# --- Global Values ---
DEVELOPER_KEY = config.DEV_API_KEY["KEY"]

allCreatorsList = []
allVideosList = []

lastPullDate = [""]

deletableCreatorsList = []
deletableVideosList = []

addableCreatorsList = []
addableVideosList = []


def deleteCreator(creator: Creator):
    deletableCreatorsList.append(creator)


def deleteVideo(video: Video):
    deletableVideosList.append(video)
    fixVideoCounter()


def addToVideoCounter(creatorID: str):
    for creator in allCreatorsList:
        if creator.creatorID.strip() == creatorID.strip():
            creator.videoCounter += 1


def getID_APICall_(contentCreator: str) -> typing.Tuple[str, str, str]:
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "0"

    api_service_name = "youtube"
    api_version = "v3"

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = DEVELOPER_KEY)

    request = youtube.channels().list(
        part="snippet, contentDetails",
        forUsername=contentCreator,
        maxResults=1                   # 50 is max we are allowed to call!
    )
    response = request.execute()

    creatorName = (((response['items'])[0])['snippet'])['title']
    creatorID = ((response['items'])[0])['id']
    imageURL = (((((response['items'])[0])['snippet'])['thumbnails'])['medium'])['url']
    return creatorName, creatorID, imageURL


def getName_APICall_(creatorID: str) -> typing.Tuple[str, str, str]:
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "0"

    api_service_name = "youtube"
    api_version = "v3"

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = DEVELOPER_KEY)

    request = youtube.channels().list(
        part="snippet, contentDetails",
        id=creatorID,
        maxResults=1                   # 50 is max we are allowed to call!
    )
    response = request.execute()

    creatorName = (((response['items'])[0])['snippet'])['title']
    creatorUsername = (((response['items'])[0])['snippet'])['customUrl']
    imageURL = (((((response['items'])[0])['snippet'])['thumbnails'])['medium'])['url']
    return creatorName, creatorUsername, imageURL


# Get videoID -> https://www.youtube.com/watch?v=videoID
# Ex XSg9C8JbmZU -> https://www.youtube.com/watch?v=XSg9C8JbmZU
def getLatestVideos_APICall_(channelID: str, startDate: str, endDate: str):

    if isinstance(startDate, list):
        startDate = startDate[0]

    pageToken = ""

    while pageToken is not None:

        # Disable OAuthlib's HTTPS verification when running locally.
        # *DO NOT* leave this option enabled in production.
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "0"

        api_service_name = "youtube"
        api_version = "v3"

        youtube = googleapiclient.discovery.build(
            api_service_name, api_version, developerKey = DEVELOPER_KEY)

        request = youtube.search().list(
            part="snippet",
            channelId=channelID,
            maxResults=50,
            order="date",
            pageToken=pageToken,
            publishedAfter=startDate,
            publishedBefore=endDate
        )

        response = request.execute()

        itemsList = response['items']

        for item in itemsList:
            try:
                userName = (item['snippet'])['channelTitle']
                title = (item['snippet'])['title']
                videoID = (item['id'])['videoId']
                imageURL = (((item['snippet'])['thumbnails'])['medium'])['url']
                dateUploaded = (item['snippet'])['publishTime']

                video = Video(userName, title, videoID, imageURL, dateUploaded, channelID)
                allVideosList.append(video)
                addableVideosList.append(video)

                addToVideoCounter(userName)

            except Exception:
                pass

        if "nextPageToken" in response:
            pageToken = response['nextPageToken']
        else:
            pageToken = None


def addCreator(name: str):
    isInList = False

    for creator in allCreatorsList:
        if name is creator.userName:
            isInList = True
            break

    if isInList is False:
        api_results = getID_APICall_(name)
        creator = Creator(api_results[0], name, api_results[1], 0,
                          (datetime.datetime.now()).strftime("%Y-%m-%dT%H:%M:%SZ"), api_results[2])
        allCreatorsList.append(creator)
        addableCreatorsList.append(creator)


def addCreator_ByID(id: str):
    isInList = False

    for creator in allCreatorsList:
        if id is creator.creatorID:
            isInList = True
            break

    if isInList is False:
        api_results = getName_APICall_(id)
        creator = Creator(api_results[0], api_results[1], id, 0,
                          (datetime.datetime.now()).strftime("%Y-%m-%dT%H:%M:%SZ"), api_results[2])
        allCreatorsList.append(creator)
        addableCreatorsList.append(creator)


def save():

    # Ensure DB is created
    if database.doesDBExist(os.getcwd()) is not True:
        database.createDB()

    # Delete items selected to be removed
    if len(deletableCreatorsList) is not 0:
        for creator in deletableCreatorsList:
            allCreatorsList.remove(creator)
            if creator in addableCreatorsList:
                addableCreatorsList.remove(creator)
            else:
                database.deleteFromCreator(creator.creatorID)

    if len(deletableVideosList) is not 0:
        for video in deletableVideosList:
            allVideosList.remove(video)
            if video in addableVideosList:
                addableVideosList.remove(video)
            else:
                database.deleteFromVideo(video.videoID)

    deletableCreatorsList.clear()
    deletableVideosList.clear()

    # Add all new items
    if len(addableCreatorsList) is not 0:
        for creator in addableCreatorsList:
            database.addCreatorToTable(creator)

    if len(addableVideosList) is not 0:
        for video in addableVideosList:
            database.addVideoToTable(video)

    addableCreatorsList.clear()
    addableVideosList.clear()

    # Update last pull date if applicable
    if lastPullDate[0] is not database.loadPullDate():
        database.updatePullDate(lastPullDate[0])


def load():

    print (os.getcwd())

    # Ensure DB is created
    if database.doesDBExist(os.getcwd()) is not True:
        database.createDB()

    # Clear out all local lists
    allCreatorsList.clear()
    allVideosList.clear()
    deletableCreatorsList.clear()
    deletableVideosList.clear()
    addableCreatorsList.clear()
    addableVideosList.clear()

    # Load in creators
    for row in database.loadInCreatorTable():
        allCreatorsList.append(Creator(row[0], row[1], row[2], row[3], row[4], row[5]))

    # Load in videos
    for row in database.loadInVideoTable():
        allVideosList.append(Video(row[0], row[1], row[2], row[3], row[4], row[5]))

    # Load in last pull date
    date = database.loadPullDate()
    if not date or date is "":
        lastPullDate[0] = (datetime.datetime.now()).strftime("%Y-%m-%dT%H:%M:%SZ")
    else:
        lastPullDate[0] = date

    fixVideoCounter()


def fixVideoCounter():
    for creator in allCreatorsList:
        creator.videoCounter = 0

    for video in allVideosList:
        if video not in deletableVideosList:
            addToVideoCounter(video.creatorID)


def pullVideos():

    startPullDate = lastPullDate[0]
    endPullDate = (datetime.datetime.now()).strftime("%Y-%m-%dT%H:%M:%SZ")

    for creator in allCreatorsList:
        getLatestVideos_APICall_(creator.creatorID, startPullDate, endPullDate)

    lastPullDate[0] = endPullDate

    videosList = list(dict.fromkeys(allVideosList))
    allVideosList.clear()

    for video in videosList:
        allVideosList.append(video)

    fixVideoCounter()


def sortCreatorByName():
    allCreatorsList.sort(key=lambda creator: creator.name)


def sortCreatorByVideos():
    allCreatorsList.sort(key=lambda creator: (creator.videoCounter, creator.name))


def sortCreatorByDate():
    allCreatorsList.sort(key=lambda creator: creator.dateAdded)


def sortVideoByCreator():
    allVideosList.sort(key=lambda video: (video.userName, video.dateUploaded))


def sortVideoByTitle():
    allVideosList.sort(key=lambda video: video.title)


def sortVideoByDate():
    allVideosList.sort(key=lambda video: video.dateUploaded)


def resetToDefault():
    allCreatorsList.clear()
    allVideosList.clear()
    lastPullDate[0] = (datetime.datetime.now()).strftime("%Y-%m-%dT%H:%M:%SZ")


# if __name__ == "__main__":
#     print("Doing nothing to help prevent accidental API calls.")
#     lastPullDate[0] = "2020-10-10T19:23:01Z"
#     addCreator("gordonramsay")
#     addCreator_ByID("UCdoPCztTOW7BJUPk2h5ttXA")
#     pullVideos()
#     load()
#     addCreator("SSoHPKC")
#     save()
#     pullVideos()
#     sortVideoByDate()
#     save()

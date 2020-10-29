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


def deleteCreator(creatorList: typing.List[Creator]):
    for creator in creatorList:
        allCreatorsList.remove(creator)
        deletableCreatorsList.append(creator)


def deleteVideo(videoList: typing.List[Video]):
    for video in videoList:
        allVideosList.remove(video)
        deletableVideosList.append(video)

    fixVideoCounter()


def addToVideoCounter(userName: str):
    for creator in allCreatorsList:
        if creator.userName.strip() == userName.strip():
            creator.videoCounter += 1


def getID_APICall_(contentCreator: str):
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "0"

    api_service_name = "youtube"
    api_version = "v3"

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = DEVELOPER_KEY)

    request = youtube.channels().list(
        part="contentDetails",
        forUsername=contentCreator,
        maxResults=1                   # 50 is max we are allowed to call!
    )
    response = request.execute()

    creatorID = ((response['items'])[0])['id']
    return creatorID


# Get videoID -> https://www.youtube.com/watch?v=videoID
# Ex XSg9C8JbmZU -> https://www.youtube.com/watch?v=XSg9C8JbmZU
def getLatestVideos_APICall_(channelID: str, startDate: str, endDate: str):

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
            userName = (item['snippet'])['channelTitle']
            title = (item['snippet'])['title']
            videoID = (item['id'])['videoId']
            imageURL = (((item['snippet'])['thumbnails'])['medium'])['url']
            dateUploaded = (item['snippet'])['publishTime']

            video = Video(userName, title, videoID, imageURL, dateUploaded)
            allVideosList.append(video)
            addableVideosList.append(video)

            addToVideoCounter(userName)

        if "nextPageToken" in response:
            pageToken = response['nextPageToken']
        else:
            pageToken = None


def addCreator(name: str):
    flag = False

    for creator in allCreatorsList:
        if name is creator.userName:
            flag = True

    if flag is False:
        creator = Creator(name, getID_APICall_(name), 0, (datetime.datetime.now()).strftime("%Y-%m-%dT%H:%M:%SZ"))
        allCreatorsList.append(creator)
        addableCreatorsList.append(creator)


def save():

    # Ensure DB is created
    if database.doesDBExist() is not True:
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
    if database.doesDBExist() is not True:
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
        allCreatorsList.append(Creator(row[0], row[1], row[2], row[3]))

    # Load in videos
    for row in database.loadInVideoTable():
        allVideosList.append(Video(row[0], row[1], row[2], row[3], row[4]))

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
        addToVideoCounter(video.userName)


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
    allCreatorsList.sort(key=lambda creator: creator.userName)


def sortCreatorByVideos():
    allCreatorsList.sort(key=lambda creator: creator.videoCounter)


def sortCreatorByDate():
    allCreatorsList.sort(key=lambda creator: creator.dateAdded)


def sortVideoByCreator():
    allVideosList.sort(key=lambda video: video.userName)


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
#     addCreator("SSoHPKC")
#     save()
#     pullVideos()
#     sortVideoByDate()
#     save()

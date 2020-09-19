# -*- coding: utf-8 -*-

# Sample Python code for youtube.channels.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

import os
import datetime
import googleapiclient.discovery
import config
import typing


# --- Global Values ---
DEVELOPER_KEY = config.DEV_API_KEY["KEY"]
DEV_ITEM_SPLIT = "<!--Comma---,---Comma--!>"
DEV_OBJ_SPLIT = "<!--Semicolon---;---Semicolon--!>"
allCreatorsList = []
allVideosList = []
lastPullDate = []


class Creator:
    def __init__(self, userName: str, creatorID: str, videoCounter: int, dateAdded: str):
        self.userName = userName
        self.creatorID = creatorID.strip()
        self.videoCounter = videoCounter
        self.dateAdded = dateAdded.strip()
        allCreatorsList.append(self)

        print(userName, " ", creatorID, " ", videoCounter, " ", dateAdded)


class Video:
    def __init__(self, userName: str, title: str, videoID: str, imageURL: str, dateUploaded: str):
        self.userName = userName
        self.title = title
        self.videoID = videoID.strip()
        self.videoURL = "https://www.youtube.com/watch?v=" + videoID.strip()
        self.imageURL = imageURL.strip()
        self.dateUploaded = dateUploaded.strip()
        allVideosList.append(self)

        print(userName, " ", title, " ", videoID, " ", imageURL, " ", dateUploaded, "\n")


def deleteCreator(creatorList: typing.List[Creator]):
    for creator in creatorList:
        allCreatorsList.remove(creator)


def deleteVideo(videoList: typing.List[Video]):
    for video in videoList:
        allVideosList.remove(video)

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

            Video(userName, title, videoID, imageURL, dateUploaded)
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
        Creator(name, getID_APICall_(name), 0, (datetime.datetime.now()).strftime("%Y-%m-%dT%H:%M:%SZ"))


def save():
    if os.path.exists("saveCreators.txt"):
        os.remove("saveCreators.txt")

    if os.path.exists("saveVideos.txt"):
        os.remove("saveVideos.txt")

    if os.path.exists("saveDate.txt"):
        os.remove("saveDate.txt")

    fileCreators = open("saveCreators.txt", "a")
    fileVideos = open("saveVideos.txt", "a")
    fileDate = open("saveDate.txt", "a")

    fixVideoCounter()

    for creator in allCreatorsList:
        strCreator = creator.userName + DEV_ITEM_SPLIT + creator.creatorID + DEV_ITEM_SPLIT + str(creator.videoCounter) + DEV_ITEM_SPLIT + creator.dateAdded + DEV_OBJ_SPLIT
        fileCreators.write(strCreator)

    for video in allVideosList:
        strVideo = video.userName + DEV_ITEM_SPLIT + video.title + DEV_ITEM_SPLIT + video.videoID + DEV_ITEM_SPLIT + video.imageURL + DEV_ITEM_SPLIT + video.dateUploaded + DEV_OBJ_SPLIT
        fileVideos.write(strVideo)

    if len(lastPullDate) != 0:
        fileDate.write(lastPullDate[0])
    else:
        fileDate.write("")

    fileCreators.close()
    fileVideos.close()
    fileDate.close()


def load():
    allCreatorsList.clear()
    allVideosList.clear()

    if os.path.exists("saveCreators.txt"):
        fileCreators = open("saveCreators.txt", "r").read()
        listCreators = fileCreators.split(DEV_OBJ_SPLIT)

        for creator in listCreators:
            if creator is not "":
                listCreatorItems = creator.split(DEV_ITEM_SPLIT)
                Creator(listCreatorItems[0], listCreatorItems[1], int(listCreatorItems[2]), listCreatorItems[3])

    if os.path.exists("saveVideos.txt"):
        fileVideos = open("saveVideos.txt", "r").read()
        listVideos = fileVideos.split(DEV_OBJ_SPLIT)

        for video in listVideos:
            if video is not "":
                listVideoItem = video.split(DEV_ITEM_SPLIT)
                Video(listVideoItem[0], listVideoItem[1], listVideoItem[2], listVideoItem[3], listVideoItem[4])

    lastPullDate.clear()
    if os.path.exists("saveDate.txt"):
        lastPullDate.append(open("saveDate.txt", "r").read())
        if lastPullDate[0] == "":
            lastPullDate[0] = "2020-08-13T00:00:00Z"
    else:
        lastPullDate.append("2020-08-13T00:00:00Z")

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


if __name__ == "__main__":
    print("Doing nothing to help prevent accidental API calls.")
    #addCreator("SSoHPKC")
    load()
    #save()
    #pullVideos()
    sortVideoByDate()
    save()

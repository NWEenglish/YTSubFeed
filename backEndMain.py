# -*- coding: utf-8 -*-

# Sample Python code for youtube.channels.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

import os
import datetime
import googleapiclient.discovery


# --- Global Values ---
DEVELOPER_KEY = "***REMOVED***"
allCreatorsList = []
allVideos = []


class NewCreator:
    def __init__(self, userName: str, ID: str, videoCounter: int, dateAdded: str):
        self.userName = userName
        self.ID = ID
        self.videoCounter = videoCounter
        self.dateAdded = dateAdded
        allCreatorsList.append(self)

        #print(userName, " ", ID, " ", videoCounter, " ", dateAdded)


class NewVideo:
    def __init__(self, userName: str, title: str, videoID: str, imageURL: str, dateUploaded: str):
        self.userName = userName
        self.title = title
        self.videoURL = "https://www.youtube.com/watch?v=" + videoID
        self.imageURL = imageURL
        self.dateUploaded = dateUploaded
        addToVideoCounter(userName)
        allVideos.append(self)

        #print(userName, " ", title, " ", self.videoURL, " ", imageURL, " ", dateUploaded, "\n")


def addToVideoCounter(userName: str):
    for creator in allCreatorsList:
        if creator.userName == userName:
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

            NewVideo(userName, title, videoID, imageURL, dateUploaded)

        if "nextPageToken" in response:
            pageToken = response['nextPageToken']
        else:
            pageToken = None


def createCreator(name: str):
    return NewCreator(name, getID_APICall_(name), 0, datetime.date.today())


if __name__ == "__main__":
    print("Doing nothing to help prevent accidental API calls.")

    # --- Sample API calls that return data ---
    # getLatestVideos_APICall_("UCVdtW2E4vwvf8yh4FY5us9A", "2020-08-13T00:00:00Z", "2020-12-12T00:00:00Z")
    # getID_APICall_("SSoHPKC")

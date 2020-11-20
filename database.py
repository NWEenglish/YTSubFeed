import os
import sqlite3
from CreatorAndVideoObjects import Creator, Video


def loadPullDate() -> str:
    myDB = sqlite3.connect("myYTSFDB.db")
    myCursor = myDB.cursor()

    try:
        myCursor.execute("SELECT * FROM pullDateTable")

    except Exception:
        myCursor.execute("CREATE TABLE pullDateTable (date text)")
        return ""

    myResult = myCursor.fetchall()

    if len(myResult) is 0:
        return ""

    else:
        return myResult[0]


def updatePullDate(date: str):
    myDB = sqlite3.connect("myYTSFDB.db")
    myCursor = myDB.cursor()

    myCursor.execute("DELETE FROM pullDateTable")
    myCursor.execute("INSERT INTO pullDateTable VALUES (?)", (date[0],))

    myDB.commit()
    myDB.close()


def loadInVideoTable() -> list:
    myDB = sqlite3.connect("myYTSFDB.db")
    myCursor = myDB.cursor()

    try:
        myCursor.execute("SELECT * FROM videoTable")
        myResult = myCursor.fetchall()
        return myResult

    except Exception:
        return []


def loadInCreatorTable() -> list:
    myDB = sqlite3.connect("myYTSFDB.db")
    myCursor = myDB.cursor()

    try:
        myCursor.execute("SELECT * FROM creatorTable")
        myResult = myCursor.fetchall()
        return myResult

    except Exception:
        return []


def addCreatorToTable(creator: Creator):
    myDB = sqlite3.connect("myYTSFDB.db")
    myCursor = myDB.cursor()

    try:
        myCursor.execute("INSERT INTO creatorTable (name, userName, creatorID, videoCounter, dateAdded, imageURL) "
                         "VALUES (?, ?, ?, ?, ?, ?)",
                         (creator.name, creator.userName, creator.creatorID, creator.videoCounter, creator.dateAdded,
                          creator.imageURL))

    except Exception:
        createCreatorTable(myCursor)

        myCursor.execute("INSERT INTO creatorTable (name, userName, creatorID, videoCounter, dateAdded, imageURL) "
                         "VALUES (?, ?, ?, ?, ?, ?)",
                         (creator.name, creator.userName, creator.creatorID, creator.videoCounter, creator.dateAdded,
                          creator.imageURL))

    myDB.commit()
    myDB.close()


def addVideoToTable(video: Video):
    myDB = sqlite3.connect("myYTSFDB.db")
    myCursor = myDB.cursor()

    try:
        myCursor.execute("INSERT INTO videoTable (name, title, videoID, imageURL, dateUploaded, creatorID) "
                         "VALUES (?, ?, ?, ?, ?, ?)",
                         (video.name, video.title, video.videoID, video.imageURL, video.dateUploaded, video.creatorID))

    except Exception:
        createVideoTable(myCursor)

        myCursor.execute("INSERT INTO videoTable (name, title, videoID, imageURL, dateUploaded, creatorID) "
                         "VALUES (?, ?, ?, ?, ?, ?)",
                         (video.name, video.title, video.videoID, video.imageURL, video.dateUploaded, video.creatorID))

    myDB.commit()
    myDB.close()


def createDB():
    myDB = sqlite3.connect("myYTSFDB.db")
    myCursor = myDB.cursor()

    createVideoTable(myCursor)
    createCreatorTable(myCursor)

    myCursor.execute("CREATE TABLE pullDateTable (date text)")

    myDB.commit()
    myDB.close()


def createCreatorTable(myCursor):
    myCursor.execute("""CREATE TABLE IF NOT EXISTS creatorTable ( 
                     name text,
                     userName text,
                     creatorID text PRIMARY KEY,
                     videoCounter integer,
                     dateAdded text,
                     imageURL text
                     )""")


def createVideoTable(myCursor):
    myCursor.execute("""CREATE TABLE IF NOT EXISTS videoTable ( 
                     name text,
                     title text,
                     videoID text PRIMARY KEY,
                     imageURL text,
                     dateUploaded text,
                     creatorID text
                     )""")


def doesDBExist(filePath: str) -> bool:
    return os.path.isfile(filePath + "\\myYTSFDB.db")


def clearAllTables():
    myDB = sqlite3.connect("myYTSFDB.db")

    myCursor = myDB.cursor()
    myCursor.execute("DELETE FROM videoTable")
    myCursor.execute("DELETE FROM creatorTable")
    myDB.commit()
    myDB.close()


def deleteFromCreator(creatorID: str):
    myDB = sqlite3.connect("myYTSFDB.db")

    myCursor = myDB.cursor()
    myCursor.execute("DELETE FROM creatorTable WHERE creatorID = (?)", (creatorID,))

    myDB.commit()
    myDB.close()


def deleteFromVideo(videoID: str):
    myDB = sqlite3.connect("myYTSFDB.db")

    myCursor = myDB.cursor()
    myCursor.execute("DELETE FROM videoTable WHERE videoID = (?)", (videoID,))

    myDB.commit()
    myDB.close()

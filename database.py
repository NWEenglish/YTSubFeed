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
    myCursor.execute("INSERT INTO pullDateTable VALUES (?)", (date,))

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
        myCursor.execute("INSERT INTO creatorTable (userName, creatorID, videoCounter, dateAdded) "
                         "VALUES (?, ?, ?, ?)",
                         (creator.userName, creator.creatorID, creator.videoCounter, creator.dateAdded))

    except Exception:
        myCursor.execute("""CREATE TABLE IF NOT EXISTS creatorTable ( 
                         userName text,
                         title text,
                         videoID text PRIMARY KEY,
                         imageURL text,
                         dateUploaded text 
                         )""")

        myCursor.execute("INSERT INTO creatorTable (userName, creatorID, videoCounter, dateAdded) "
                         "VALUES (?, ?, ?, ?)",
                         (creator.userName, creator.creatorID, creator.videoCounter, creator.dateAdded))

    myDB.commit()
    myDB.close()


def addVideoToTable(video: Video):
    myDB = sqlite3.connect("myYTSFDB.db")
    myCursor = myDB.cursor()

    try:
        myCursor.execute("INSERT INTO videoTable (userName, title, videoID, imageURL, dateUploaded) "
                         "VALUES (?, ?, ?, ?, ?)",
                         (video.userName, video.title, video.videoID, video.imageURL, video.dateUploaded))

    except Exception:
        myCursor.execute("""CREATE TABLE IF NOT EXISTS videoTable ( 
                         userName text, 
                         creatorID text PRIMARY KEY, 
                         videoCounter integer, 
                         dateAdded text 
                         )""")

        myCursor.execute("INSERT INTO videoTable (userName, title, videoID, imageURL, dateUploaded) "
                         "VALUES (?, ?, ?, ?, ?)",
                         (video.userName, video.title, video.videoID, video.imageURL, video.dateUploaded))

    myDB.commit()
    myDB.close()


def createDB():
    myDB = sqlite3.connect("myYTSFDB.db")

    myCursor = myDB.cursor()

    myCursor.execute("""CREATE TABLE videoTable ( 
                     userName text, 
                     creatorID text PRIMARY KEY, 
                     videoCounter integer, 
                     dateAdded text 
                     )""")

    myCursor.execute("""CREATE TABLE creatorTable ( 
                     userName text,
                     title text,
                     videoID text PRIMARY KEY,
                     imageURL text,
                     dateUploaded text 
                     )""")

    myCursor.execute("CREATE TABLE pullDateTable (date text)")

    myDB.commit()
    myDB.close()


# def createVideoTableIfNotExist():
#     myDB = sqlite3.connect("myYTSFDB.db")
#
#     myCursor = myDB.cursor()
#
#     myCursor.execute("CREATE TABLE videoTable ( "
#                      "userName VARCHAR(255), "
#                      "creatorID VARCHAR(255), "
#                      "videoCounter INT, "
#                      "dateAdded VARCHAR(255) )")


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
    myCursor.execute("DELETE FROM creatorTable WHERE creatorID = ?", creatorID)

    myDB.commit()
    myDB.close()


def deleteFromVideo(videoID: str):
    myDB = sqlite3.connect("myYTSFDB.db")

    myCursor = myDB.cursor()
    myCursor.execute("DELETE FROM videoTable WHERE videoID = ?", videoID)

    myDB.commit()
    myDB.close()


# if __name__ == "__main__":
#
#     print("Begin")
#     # createDB()
#
#     myDB1 = sqlite3.connect("myYTSFDB.db")
#
#     myCursor1 = myDB1.cursor()
#     myCursor1.execute("SELECT * FROM pullDateTable")
#
#     myResult1 = myCursor1.fetchall()
#
#     for r in myResult1:
#         print(r)

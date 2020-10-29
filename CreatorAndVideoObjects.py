class Creator:
    def __init__(self, userName: str, creatorID: str, videoCounter: int, dateAdded: str):
        self.userName = userName
        self.creatorID = creatorID.strip()
        self.videoCounter = videoCounter
        self.dateAdded = dateAdded.strip()

        print(userName, " ", creatorID, " ", videoCounter, " ", dateAdded)


class Video:
    def __init__(self, userName: str, title: str, videoID: str, imageURL: str, dateUploaded: str):
        self.userName = userName
        self.title = title.replace("&#39;", "\'")
        self.videoID = videoID.strip()
        self.videoURL = "https://www.youtube.com/watch?v=" + videoID.strip()
        self.imageURL = imageURL.strip()
        self.dateUploaded = dateUploaded.strip()

        print(userName, " ", title, " ", videoID, " ", imageURL, " ", dateUploaded, "\n")

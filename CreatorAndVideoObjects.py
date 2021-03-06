class Creator:
    def __init__(self, name: str, userName: str, creatorID: str, videoCounter: int, dateAdded: str, imageURL: str):
        self.name = name;
        self.userName = userName
        self.creatorID = creatorID.strip()
        self.videoCounter = videoCounter
        self.dateAdded = dateAdded.strip()
        self.imageURL = imageURL.strip()
        self.channelURL = "https://www.youtube.com/channel/" + creatorID.strip()


class Video:
    def __init__(self, name: str, title: str, videoID: str, imageURL: str, dateUploaded: str, creatorID: str):
        self.name = name
        self.title = title.replace("&#39;", "\'").replace("&amp;", "&")
        self.videoID = videoID.strip()
        self.videoURL = "https://www.youtube.com/watch?v=" + videoID.strip()
        self.imageURL = imageURL.strip()
        self.dateUploaded = dateUploaded.strip()
        self.creatorID = creatorID.strip()

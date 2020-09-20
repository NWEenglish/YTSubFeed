import unittest
import sys
import os
sys.path.append(os.path.abspath("./"))
import backEndMain

# Flip this to True if we need to run tests with API calls
runAPICalls = False


class BackEndTests(unittest.TestCase):

    def tearDown(self):
        backEndMain.allCreatorsList.clear()
        backEndMain.allVideosList.clear()

    def test_CreatorObject(self):
        # Arrange
        userName = "Tester"
        creatorID = "1234"
        videoCounter = 7
        dateAdded = "2020-01-01"

        # Act
        result = backEndMain.Creator(userName, creatorID, videoCounter, dateAdded)

        # Assert
        self.assertEqual(result.userName, userName)
        self.assertEqual(result.creatorID, creatorID)
        self.assertEqual(result.videoCounter, videoCounter)
        self.assertEqual(result.dateAdded, dateAdded)

    def test_VideoObject(self):
        # Arrange
        userName = "Tester"
        title = "Video Title"
        videoID = "1234"
        imageURL = "www.google.com"
        dateUploaded = "2020-01-01"

        # Act
        result = backEndMain.Video(userName, title, videoID, imageURL, dateUploaded)

        # Assert
        self.assertEqual(result.userName, userName)
        self.assertEqual(result.title, title)
        self.assertEqual(result.videoID, videoID)
        self.assertEqual(result.imageURL, imageURL)
        self.assertEqual(result.dateUploaded, dateUploaded)

    def test_VideoObject_WithApostropheInTitle(self):
        # Arrange
        userName = "Tester"
        title = "Video Title&#39;s"
        videoID = "1234"
        imageURL = "www.google.com"
        dateUploaded = "2020-01-01"

        # Act
        result = backEndMain.Video(userName, title, videoID, imageURL, dateUploaded)

        # Assert
        self.assertEqual(result.userName, userName)
        self.assertEqual(result.title, "Video Title\'s")
        self.assertEqual(result.videoID, videoID)
        self.assertEqual(result.imageURL, imageURL)
        self.assertEqual(result.dateUploaded, dateUploaded)

    def test_DeleteCreator(self):
        # Arrange
        creator = backEndMain.Creator("Tester", "1234", 7, "2020-01-01")

        # Act
        backEndMain.deleteCreator([creator])

        # Assert
        self.assertEqual(len(backEndMain.allCreatorsList), 0)

    def test_DeleteVideo(self):
        # Arrange
        video = backEndMain.Video("Tester", "Video Title", "1234", "www.google.com", "2020-01-01")

        # Act
        backEndMain.deleteVideo([video])

        # Assert
        self.assertEqual(len(backEndMain.allVideosList), 0)

    def test_FixVideoCounter(self):
        # Arrange
        creator = backEndMain.Creator("Tester", "1234", 7, "2020-01-01")
        video = backEndMain.Video(creator.userName, "Video Title", "1234", "www.google.com", "2020-01-01")

        # Act
        backEndMain.fixVideoCounter()

        # Assert
        self.assertEqual(creator.videoCounter, 1)

    def test_AddToVideoCounter(self):
        # Arrange
        creator = backEndMain.Creator("Tester", "1234", 7, "2020-01-01")

        # Act
        backEndMain.addToVideoCounter(creator.userName)

        # Assert
        self.assertEqual(creator.videoCounter, 8)

    def test_AddCreator_NotInList(self):

        if runAPICalls is True:
            # Act
            backEndMain.addCreator("Youtube")

            # Assert
            self.assertEqual(len(backEndMain.allCreatorsList), 1)

    def test_AddCreator_AlreadyInList(self):

        if runAPICalls is True:
            # Arrange
            backEndMain.Creator("Youtube", "1234", 7, "2020-01-01")

            # Act
            backEndMain.addCreator("Youtube")

            # Assert
            self.assertEqual(len(backEndMain.allCreatorsList), 1)

    def test_SortCreatorByName_CorrectOrder(self):
        # Arrange
        creatorA = backEndMain.Creator("A", "1234", 7, "2020-01-01")
        creatorB = backEndMain.Creator("B", "1234", 7, "2020-01-01")

        # Act
        backEndMain.sortCreatorByName()

        # Assert
        self.assertEqual(backEndMain.allCreatorsList[0], creatorA)
        self.assertEqual(backEndMain.allCreatorsList[1], creatorB)

    def test_SortCreatorByName_IncorrectOrder(self):
        # Arrange
        creatorB = backEndMain.Creator("B", "1234", 7, "2020-01-01")
        creatorA = backEndMain.Creator("A", "1234", 7, "2020-01-01")

        # Act
        backEndMain.sortCreatorByName()

        # Assert
        self.assertEqual(backEndMain.allCreatorsList[0], creatorA)
        self.assertEqual(backEndMain.allCreatorsList[1], creatorB)

    def test_SortCreatorByVideos_CorrectOrder(self):
        # Arrange
        creatorA = backEndMain.Creator("A", "1234", 1, "2020-01-01")
        creatorB = backEndMain.Creator("B", "1234", 10, "2020-01-01")

        # Act
        backEndMain.sortCreatorByVideos()

        # Assert
        self.assertEqual(backEndMain.allCreatorsList[0], creatorA)
        self.assertEqual(backEndMain.allCreatorsList[1], creatorB)

    def test_SortCreatorByVideo_IncorrectOrder(self):
        # Arrange
        creatorB = backEndMain.Creator("B", "1234", 10, "2020-01-01")
        creatorA = backEndMain.Creator("A", "1234", 1, "2020-01-01")

        # Act
        backEndMain.sortCreatorByVideos()

        # Assert
        self.assertEqual(backEndMain.allCreatorsList[0], creatorA)
        self.assertEqual(backEndMain.allCreatorsList[1], creatorB)

    def test_SortCreatorByDate_CorrectOrder(self):
        # Arrange
        creatorA = backEndMain.Creator("A", "1234", 7, "2020-01-01")
        creatorB = backEndMain.Creator("B", "1234", 7, "2020-01-02")

        # Act
        backEndMain.sortCreatorByDate()

        # Assert
        self.assertEqual(backEndMain.allCreatorsList[0], creatorA)
        self.assertEqual(backEndMain.allCreatorsList[1], creatorB)

    def test_SortCreatorByDate_IncorrectOrder(self):
        # Arrange
        creatorB = backEndMain.Creator("B", "1234", 7, "2020-01-02")
        creatorA = backEndMain.Creator("A", "1234", 7, "2020-01-01")

        # Act
        backEndMain.sortCreatorByDate()

        # Assert
        self.assertEqual(backEndMain.allCreatorsList[0], creatorA)
        self.assertEqual(backEndMain.allCreatorsList[1], creatorB)

    def test_SortVideoByCreator_CorrectOrder(self):
        # Arrange
        videoA = backEndMain.Video("A", "Title A", "1234", "www.google.com", "2020-01-01")
        videoB = backEndMain.Video("B", "Title B", "1234", "www.youtube.com", "2020-01-01")

        # Act
        backEndMain.sortVideoByCreator()

        # Assert
        self.assertEqual(backEndMain.allVideosList[0], videoA)
        self.assertEqual(backEndMain.allVideosList[1], videoB)

    def test_SortVideoByCreator_IncorrectOrder(self):
        # Arrange
        videoB = backEndMain.Video("B", "Title B", "1234", "www.google.com", "2020-01-01")
        videoA = backEndMain.Video("A", "Title A", "1234", "www.youtube.com", "2020-01-01")

        # Act
        backEndMain.sortVideoByCreator()

        # Assert
        self.assertEqual(backEndMain.allVideosList[0], videoA)
        self.assertEqual(backEndMain.allVideosList[1], videoB)

    def test_SortVideoByTitle_CorrectOrder(self):
        # Arrange
        videoA = backEndMain.Video("A", "Title A", "1234", "www.google.com", "2020-01-01")
        videoB = backEndMain.Video("B", "Title B", "1234", "www.youtube.com", "2020-01-01")

        # Act
        backEndMain.sortVideoByTitle()

        # Assert
        self.assertEqual(backEndMain.allVideosList[0], videoA)
        self.assertEqual(backEndMain.allVideosList[1], videoB)

    def test_SortVideoByTitle_IncorrectOrder(self):
        # Arrange
        videoB = backEndMain.Video("B", "Title B", "1234", "www.google.com", "2020-01-01")
        videoA = backEndMain.Video("A", "Title A", "1234", "www.youtube.com", "2020-01-01")

        # Act
        backEndMain.sortVideoByTitle()

        # Assert
        self.assertEqual(backEndMain.allVideosList[0], videoA)
        self.assertEqual(backEndMain.allVideosList[1], videoB)

    def test_SortVideoByDate_CorrectOrder(self):
        # Arrange
        videoA = backEndMain.Video("A", "Title A", "1234", "www.google.com", "2020-01-01")
        videoB = backEndMain.Video("B", "Title B", "1234", "www.youtube.com", "2020-01-02")

        # Act
        backEndMain.sortVideoByDate()

        # Assert
        self.assertEqual(backEndMain.allVideosList[0], videoA)
        self.assertEqual(backEndMain.allVideosList[1], videoB)

    def test_SortVideoByDate_IncorrectOrder(self):
        # Arrange
        videoB = backEndMain.Video("B", "Title A", "1234", "www.google.com", "2020-01-02")
        videoA = backEndMain.Video("A", "Title B", "1234", "www.youtube.com", "2020-01-01")

        # Act
        backEndMain.sortVideoByDate()

        # Assert
        self.assertEqual(backEndMain.allVideosList[0], videoA)
        self.assertEqual(backEndMain.allVideosList[1], videoB)

    def test_ResetToDefault(self):
        # Arrange
        backEndMain.Creator("Tester1", "1234", 7, "2020-01-01")
        backEndMain.Creator("Tester2", "1234", 7, "2020-01-01")
        backEndMain.Video("Tester1", "Video Title A", "1234", "www.google.com", "2020-01-01")
        backEndMain.Video("Tester2", "Video Title B", "1234", "www.youtube.com", "2020-01-01")

        # Act
        backEndMain.resetToDefault()

        # Assert
        self.assertEqual(len(backEndMain.allCreatorsList), 0)
        self.assertEqual(len(backEndMain.allVideosList), 0)

if __name__ == '__main__':
    unittest.main()

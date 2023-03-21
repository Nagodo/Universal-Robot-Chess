import cv2
from threading import Thread

class Vision:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.foundChessboard = False

    def checkForUpdates(self):
        if not self.foundChessboard:
            self.findChessboard()


    def findChessboard(self):
        pass


def startVision():
    vision = Vision()
    while True:
        ret, frame = vision.cap.read()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    vision.cap.release()
    cv2.destroyAllWindows()


visionThread = Thread(target=startVision)
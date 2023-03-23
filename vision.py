import cv2
from threading import Thread
import time

class Vision:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.foundChessboard = False

    def checkForUpdates(self):
        if not self.foundChessboard:
            self.findChessboard()


    def findChessboard(self):
        pass

    def startVision(self):
        while True:
            ret, frame = self.cap.read()

            cv2.imshow('frame', frame)

            time.sleep(2)

           

        self.cap.release()
        cv2.destroyAllWindows()




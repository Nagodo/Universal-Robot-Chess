import cv2
from threading import Thread
import time

class Vision:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.foundChessboard = False
        self.showVideo = True

    def checkForUpdates(self):
        if not self.foundChessboard:
            self.findChessboard()


    def findChessboard(self):
        pass

    def startVision(self):
        while True:
            ret, frame = self.cap.read()
            if self.showVideo:
                cv2.imshow('frame', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
        self.cap.release()
        cv2.destroyAllWindows()




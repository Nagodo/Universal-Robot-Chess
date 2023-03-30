import cv2
from threading import Thread
import time

class Vision:
    def __init__(self):
        self.cap = cv2.VideoCapture(2)
        self.showVideo = True
        self.oldframe = None
        self.newframe = None

    def checkForUpdates(self):
        print("Checking for updates")
        if self.oldframe is not None:
            #Loop through all pixels in both images

            for x in range(0, self.newframe.shape[0]):
                for y in range(0, self.newframe.shape[1]):
                    old_color = self.oldframe[x][y]
                    new_color = self.newframe[x][y]

                    is_diff = self.GetDifference(old_color, new_color)
                    if is_diff:
                        self.oldframe[x][y] = (0, 255, 0)

    def GetDifference(self, old_color, new_color):
        d_r = int(old_color[0]) - int(new_color[0])
        d_g = int(old_color[1]) - int(new_color[1])
        d_b = int(old_color[2]) - int(new_color[2])

        sum = d_r + d_g + d_b
        if sum > 35:
            return True
        
        return False
            
    def UpdateOldFrame(self):
        ret, frame = self.cap.read()
        self.oldframe = frame

    def startVision(self):
        while True:
            ret, frame = self.cap.read()
           
            if self.oldframe is not None:
                cv2.imshow('oldframe', self.oldframe)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.newframe = frame
                self.checkForUpdates()
                


    




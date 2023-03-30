import cv2
from threading import Thread
import time

class Vision:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.showVideo = True
        self.oldframe = None
        self.newframe = None

    def set_chessboard_coords(self):
        gray = cv2.cvtColor(self.oldframe, cv2.COLOR_BGR2GRAY)
        
        _, thresh = cv2.threshold(gray, 0, 250, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)
        
        second_largest_contour = contours[1]

        cv2.drawContours(self.oldframe, [second_largest_contour], -1, (0, 255, 0), 3)
        
        contour_coords = second_largest_contour[:, 0, :]
        contour_x_coords = contour_coords[:, 0]
        contour_y_coords = contour_coords[:, 1]

        min_x = min(contour_x_coords) + 36.5
        max_x = max(contour_x_coords) - 36.5
        min_y = min(contour_y_coords) + 36.5
        max_y = max(contour_y_coords) - 36.5

       
        self.chessboard_coords = (min_x, max_x, min_y, max_y)

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
        if sum > 15:
            return True
        
        return False
            
    def UpdateOldFrame(self):
        ret, frame = self.cap.read()
        self.oldframe = frame
        self.set_chessboard_coords()

    def startVision(self):
        while True:
            ret, frame = self.cap.read()
           
            if self.oldframe is not None:
                cv2.imshow('oldframe', self.oldframe)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.newframe = frame
                self.checkForUpdates()
                


    




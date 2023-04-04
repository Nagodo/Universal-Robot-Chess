import cv2
from threading import Thread
import time
import random
from CONFIG import *

class Vision:
    def __init__(self):
        self.cap = cv2.VideoCapture(2)
        self.showVideo = True
        self.oldframe = None
        self.newframe = None

    def set_chessboard_coords(self):
        gray = cv2.cvtColor(self.oldframe, cv2.COLOR_BGR2GRAY)
        
        _, thresh = cv2.threshold(gray, 0, 250, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        contours, __ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)
        
        second_largest_contour = contours[1]

        contour_coords = second_largest_contour[:, 0, :]
        contour_x_coords = contour_coords[:, 0]
        contour_y_coords = contour_coords[:, 1]

        min_x = min(contour_x_coords) + VISION_BOARD_OFFSET
        max_x = max(contour_x_coords) - VISION_BOARD_OFFSET
        min_y = min(contour_y_coords) + VISION_BOARD_OFFSET
        max_y = max(contour_y_coords) - VISION_BOARD_OFFSET

       
        self.chessboard_coords = (min_x, max_x, min_y, max_y)

        #Tegner en firkant rundt om brættet
        #cv2.rectangle(self.visualframe, (int(min_x), int(min_y)), (int(max_x), int(max_y)), (0, 255, 0), 2)

    def checkForUpdates(self):
        print("Checking for updates")
        if self.oldframe is not None:
            #Split the image into 64 squares in a dict 

            #Get the size of each square
            square_width = (self.chessboard_coords[1] - self.chessboard_coords[0]) / 8
            square_height = (self.chessboard_coords[3] - self.chessboard_coords[2]) / 8

            #Loop through each squar
            _t = False
            for x in range(0, 8):
                for y in range(0, 8):
                    #Get the coordinates of the square
                    square_x = self.chessboard_coords[0] + (square_width * x)
                    square_y = self.chessboard_coords[2] + (square_height * y)

                
                    #Get average color of the square
                    from_square_x = int(square_x + VISION_SQUARE_OFFSET)
                    from_square_y = int(square_y + VISION_SQUARE_OFFSET)
                    to_square_x = int(square_x + square_width - VISION_SQUARE_OFFSET)
                    to_square_y = int(square_y + square_height - VISION_SQUARE_OFFSET)

                    old_square_color = self.get_square_color(self.oldframe, from_square_x, from_square_y, to_square_x, to_square_y)
                    new_square_color = self.get_square_color(self.newframe, from_square_x, from_square_y, to_square_x, to_square_y)

                    if not _t:
                        cv2.imshow("Square1", self.oldframe[from_square_y:to_square_y, from_square_x:to_square_x])
                        cv2.imshow("Square2", self.newframe[from_square_y:to_square_y, from_square_x:to_square_x])

                        _t = True

                    #Check if the color has changed
                    print("Square: ", self.index_to_notation(x, y))
                    print(old_square_color, new_square_color)



            # for x in range(0, self.newframe.shape[0]):
            #     for y in range(0, self.newframe.shape[1]):
            #         old_color = self.oldframe[x][y]
            #         new_color = self.newframe[x][y]

            #         is_diff = self.GetDifference(old_color, new_color)
            #         if is_diff:
            #             self.oldframe[x][y] = (0, 255, 0)


    def get_square_color(self, frame, s_x, s_y, s_x0, s_y0):
        s_x += VISION_SQUARE_OFFSET
        s_y += VISION_SQUARE_OFFSET 
        s_x0 -= VISION_SQUARE_OFFSET
        s_y0 -= VISION_SQUARE_OFFSET
        square_color = (0, 0, 0)
        red = []
        green = []
        blue = []

        for x in range(int(s_x), int(s_x0)):
            for y in range(int(s_y), int(s_y0)):
                red.append(frame[y][x][0])
                green.append(frame[y][x][1])
                blue.append(frame[y][x][2])
        
        square_color = (sum(red) / len(red), sum(green) / len(green), sum(blue) / len(blue))

        return square_color
    
    def index_to_notation(self, x, y):
        y = 7 - y
        return chr(x + 97) + str(y + 1)

    def GetDifference(self, old_color, new_color):
        d_r = int(old_color[0]) - int(new_color[0])
        d_g = int(old_color[1]) - int(new_color[1])
        d_b = int(old_color[2]) - int(new_color[2])

        sum = d_r + d_g + d_b
        if sum > VISION_DIFF_THRESHOLD:
            return True
        
        return False
            
    def UpdateOldFrame(self):
        ret, frame = self.cap.read()
        self.oldframe = frame
        self.set_chessboard_coords()

    def startVision(self):
        while True:
            ret, frame = self.cap.read()
            if self.showVideo:
                cv2.imshow('frame', frame)
           
            if self.oldframe is not None:
                cv2.imshow('oldframe', self.oldframe)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.newframe = frame
                self.checkForUpdates()

            #If k is pressed, update the old frame
            if cv2.waitKey(1) & 0xFF == ord('k'):
                #SAVE img
                cv2.imwrite('img.png', frame)
                


    




import cv2
from threading import Thread
from skimage.metrics import structural_similarity
import pyautogui
import numpy as np
import time
import random
from CONFIG import *

class Vision:
    def __init__(self):
        self.cap = cv2.VideoCapture(2)
        self.showVideo = True
        self.oldframe = None
        self.newframe = None


    def checkForUpdates(self):
        print("Checking for updates")
        if self.oldframe is not None:
                    
            def find_green_areas(img):
                hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
                lower_green = np.array([50, 50, 50])
                upper_green = np.array([80, 255, 255])
                mask = cv2.inRange(hsv, lower_green, upper_green)
                res = cv2.bitwise_and(img, img, mask=mask)
                return res


            green1 = find_green_areas(self.oldframe)
            green2 = find_green_areas(self.newframe)

            cv2.imshow("green1", green1)
            cv2.imshow("green2", green2)
            
            def get_contours(img):
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
                contours, __ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                return contours


            def get_valid_contours(contours):
                valid_contours = []
                for c in contours:
                    area = cv2.contourArea(c)
                    if area > 8 and 100 > area:
                        valid_contours.append(c)
                return valid_contours

            c1 = get_contours(green1)
            c2 = get_contours(green2)

            c1 = get_valid_contours(c1)
            c2 = get_valid_contours(c2)

            cv2.drawContours(self.oldframe, c1, -1, (0, 255, 0), 2)
            cv2.drawContours(self.newframe, c2, -1, (0, 255, 0), 2)

            c1_coords = []
            c2_coords = []
            for c in c1:
                coord = cv2.boundingRect(c) 
                c1_coords.append((coord[0], coord[1]))
                cv2.circle(self.oldframe, (coord[0], coord[1]), 2, (0, 0, 255), 2)

            for c in c2:
                coord = cv2.boundingRect(c) 
                c2_coords.append((coord[0], coord[1]))
                cv2.circle(self.newframe, (coord[0], coord[1]), 2, (0, 0, 255), 2)


            i = 0
            final_coords = []
            for i in range(len(c1_coords)):
                found_close = False
                for j in range(len(c2_coords)):
                    dist_x = abs(c1_coords[i][0] - c2_coords[j][0])
                    dist_y = abs(c1_coords[i][1] - c2_coords[j][1])

                    if dist_x < 4.0 and dist_y < 4.0:
                        found_close = True
                        i += 1

                if not found_close:
                    final_coords.append(c1_coords[i])
                    
            cv2.imshow("old", self.oldframe)
            cv2.imshow("new", self.newframe)
            print(final_coords)
                        
    def inside_chessboard(self, x, y):
        return x > self.chessboard_coords[0] and x < self.chessboard_coords[1] and y > self.chessboard_coords[2] and y < self.chessboard_coords[3]


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

        
        sum = abs(d_r) + abs(d_g) + abs(d_b)
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
                


    




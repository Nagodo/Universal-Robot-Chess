import cv2
from skimage.metrics import structural_similarity
import numpy as np
from CONFIG import *

class Vision:
    def __init__(self):
        self.cap = cv2.VideoCapture(2)
        self.showVideo = True
        self.oldframe = None
        self.newframe = None

        self.newPlayerMove = False
        self.playerMove = ""
        self.playerMoveType = 0

        self.square_coords = {}
        for x in range(8):
            for y in range(8):
                sqr = self.c_to_sqr(x, y)
                self.square_coords[sqr] = (x*56+VISION_CHESSBOARD[0], y*56+VISION_CHESSBOARD[1])

    def c_to_sqr(self, x, y):
        return chr((97 + 7) - y) + str(8-x)

    def checkForUpdates(self):
        print("Checking for updates")

        if self.oldframe is not None:
            print("Old frame exists")
            before = cv2.cvtColor(self.oldframe, cv2.COLOR_BGR2GRAY)
            after = cv2.cvtColor(self.newframe, cv2.COLOR_BGR2GRAY)
            (score, diff) = structural_similarity(before, after, full=True)
            print("Image Similarity: {:.4f}%".format(score * 100))

            diff = (diff * 255).astype("uint8")
            diff_box = cv2.merge([diff, diff, diff])
           
            cv2.imshow('diff', diff_box)

            thress = 40
            thresh = cv2.threshold(diff, thress, 255, cv2.THRESH_BINARY_INV)[1]
            cv2.imshow('thresh', thresh)

            contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            contours = contours[0] if len(contours) == 2 else contours[1]

            mask = np.zeros(before.shape, dtype='uint8')

            contours = sorted(contours, key=cv2.contourArea, reverse=True)
            cv2.drawContours(mask, contours, -1, 255, -1)
            move_amount = 0
            out = 0, [(0,0), (0,0), (0,0), (0,0)]
            if len(contours) > 1:
                x,y,w,h = cv2.boundingRect(contours[0])
                x_2,y_2,w_2,h_2 = cv2.boundingRect(contours[1])
                cx_1 = x + w//2
                cy_1 = y + h//2
                cx_2 = x_2 + w_2//2
                cy_2 = y_2 + h_2//2
                out =  2, [(cx_1, cy_1), (cx_2, cy_2), (0,0), (0,0)]
                move_amount = 2
               

                
            move_coords = []
            for i in range (len(out[1])):
                move_coords.append(out[1][i])
                cv2.rectangle(mask, (out[1][i][0]-2, out[1][i][1]-2), (out[1][i][0]+2, out[1][i][1]+2), (255,255,255), 2)

            if move_amount == 2:
                move1 = self.GetSquareFromCoords(out[1][0][0], out[1][0][1])
                move2 = self.GetSquareFromCoords(out[1][1][0], out[1][1][1])

                self.playerMove = [move1, move2]
                self.playerMoveType = 2
                self.newPlayerMove = True


            cv2.imshow('before', mask)
    

    def GetSquareFromCoords(self, x_c, y_c):
        closest = 1000
        c_key = ""
        for key, value in self.square_coords.items():
            x = value[0]
            y = value[1]

            dist = abs(x_c - x) + abs(y_c - y)
           
            if dist < closest:
                closest = dist
                c_key = key
        return c_key
   
        
    def UpdateOldFrame(self):
        ret, frame = self.cap.read()
        self.oldframe = frame

    def startVision(self):
        while True:
            ret, frame = self.cap.read()
            if self.showVideo:
                cv2.imshow('frame', frame)
 
            if self.oldframe is not None:
                cv2.imshow('oldframe', self.oldframe)
            else:
                self.UpdateOldFrame()
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.newframe = frame
                self.checkForUpdates()



    




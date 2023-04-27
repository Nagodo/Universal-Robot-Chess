import cv2
import numpy as np


img1 = cv2.imread('img1.png')
img2 = cv2.imread('img2.png')

def find_green_areas(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    lower_green = np.array([50, 0, 50])
    upper_green = np.array([100, 255, 100])
    mask = cv2.inRange(img, lower_green, upper_green)
    res = cv2.bitwise_and(img, img, mask=mask)
    return res


green1 = find_green_areas(img1)
green2 = find_green_areas(img2)

cv2.imshow("a", green1)


def get_contours(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 100, 200, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    cv2.imshow("thresh", thresh)
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

cv2.drawContours(green1, c1, -1, (0, 255, 0), 1)
cv2.drawContours(green2, c2, -1, (0, 255, 0), 1)

cv2.imshow("a", green1)
cv2.imshow("b", green2)

c1_coords = []
c2_coords = []
for c in c1:
    coord = cv2.boundingRect(c) 
    c1_coords.append((coord[0], coord[1]))

for c in c2:
    coord = cv2.boundingRect(c) 
    c2_coords.append((coord[0], coord[1]))


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

            cv2.circle(green1, c1_coords[i-1], 3, (0, 0, 255), -1)
    
    if not found_close:
        final_coords.append(c1_coords[i])
        cv2.circle(green1, c1_coords[i], 3, (255, 0, 0), -1)
       


cv2.imshow("bdw", green1)

cv2.waitKey(0)
cv2.destroyAllWindows()
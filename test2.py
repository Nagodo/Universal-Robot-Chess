import cv2
import numpy as np
from skimage.metrics import structural_similarity


img1 = cv2.imread('img1.png')
img2 = cv2.imread('img3.png')

#Greyscale
before = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
after = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

#SSIM stuff
(score, diff) = structural_similarity(before, after, full=True)
print("Image Similarity: {:.4f}%".format(score * 100))


diff = (diff * 255).astype("uint8")
diff_box = cv2.merge([diff, diff, diff])

cv2.imshow('diff', diff_box)

thress = 40
thresh = cv2.threshold(diff, thress, 255, cv2.THRESH_BINARY_INV)[1]
cv2.imshow('thresh', thresh)
#print ("Threshold: {}".format(thresh))
contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours = contours[0] if len(contours) == 2 else contours[1]

mask = np.zeros(before.shape, dtype='uint8')
filled_after = after.copy()
contours = sorted(contours, key=cv2.contourArea, reverse=True)

out = 0, [(0,0), (0,0), (0,0), (0,0)]
if len(contours) > 1:
    if cv2.contourArea(contours[0])*0.3 < cv2.contourArea(contours[1]) < cv2.contourArea(contours[0])*1.8 and cv2.contourArea(contours[0]) > 300:
        x,y,w,h = cv2.boundingRect(contours[0])
        x_2,y_2,w_2,h_2 = cv2.boundingRect(contours[1])
        cx_1 = x + w//2
        cy_1 = y + h//2
        cx_2 = x_2 + w_2//2
        cy_2 = y_2 + h_2//2
        out =  2, [(cx_1, cy_1), (cx_2, cy_2), (0,0), (0,0)]
        if len(contours) > 3 and cv2.contourArea(contours[2])*0.3 < cv2.contourArea(contours[3]) < cv2.contourArea(contours[2])*1.8 and cv2.contourArea(contours[2]) > 300:
            x,y,w,h = cv2.boundingRect(contours[2])
            x_2,y_2,w_2,h_2 = cv2.boundingRect(contours[3])
            cx_3 = x + w//2
            cy_3 = y + h//2
            cx_4 = x_2 + w_2//2
            cy_4 = y_2 + h_2//2
            out =  4, [(cx_1, cy_1), (cx_2, cy_2), (cx_3, cy_3), (cx_4, cy_4)]
    #one piece
    elif cv2.contourArea(contours[0]) > 300 and cv2.contourArea(contours[1]) < 300:
        x,y,w,h = cv2.boundingRect(contours[0])
        cx = x + w//2
        cy = y + h//2
        out =  1, [(cx, cy), (0,0), (0,0), (0,0)]
    # four pieces
    else:
        out =  0, [(0,0), (0,0), (0,0), (0,0)]

for c in contours:
    area = cv2.contourArea(c)
    if area > 300:
        x,y,w,h = cv2.boundingRect(c)
        cv2.rectangle(before, (x, y), (x + w, y + h), (36,255,12), 2)
        cv2.rectangle(after, (x, y), (x + w, y + h), (36,255,12), 2)
        cv2.rectangle(diff_box, (x, y), (x + w, y + h), (36,255,12), 2)
        cv2.drawContours(mask, [c], 0, (100,100,100), -1)
        cv2.drawContours(filled_after, [c], 0, (0,255,0), -1)


for i in range (len(out[1])):
    cv2.rectangle(mask, (out[1][i][0]-2, out[1][i][1]-2), (out[1][i][0]+2, out[1][i][1]+2), (255,255,255), 2)

cv2.imshow('before', mask)

cv2.waitKey(0)
cv2.destroyAllWindows()
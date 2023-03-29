import cv2

# Read the image
image = cv2.imread('test1.jpg')

#Downscale the image
image = cv2.resize(image, (0,0), fx=0.25, fy=0.25)

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply thresholding to the image
_, thresh = cv2.threshold(gray, 0, 220, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)


# Find contours in the image
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

contours = sorted(contours, key=cv2.contourArea, reverse=True)

second_largest_contour = contours[1]

# Draw the contour on the original image
cv2.drawContours(image, [second_largest_contour], -1, (0, 255, 0), 3)
cv2.imshow('Contour', image)

cv2.drawContours(image, contours, -1, (0, 255, 0), 3)
cv2.imshow('Contours', image)

contour_coords = second_largest_contour[:, 0, :]
contour_x_coords = contour_coords[:, 0]
contour_y_coords = contour_coords[:, 1]


#FInd min and max x and y coords
min_x = min(contour_x_coords) + 36.5
max_x = max(contour_x_coords) - 36.5
min_y = min(contour_y_coords) + 36.5
max_y = max(contour_y_coords) - 36.5


def index_to_notation(x, y):
    y = 7 - y
    return chr(x + 97) + str(y + 1)



cv2.waitKey(0)
cv2.destroyAllWindows()
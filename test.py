import cv2

# Read the image
image = cv2.imread('test1.jpg')

#Downscale the image
image = cv2.resize(image, (0,0), fx=0.25, fy=0.25)

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


# Apply thresholding to the image
_, thresh = cv2.threshold(gray, 0, 180, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
cv2.imshow('Threshold', thresh)

# Find contours in the image
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

contours = sorted(contours, key=cv2.contourArea, reverse=True)

second_largest_contour = contours[1]

contour_coords = second_largest_contour[:, 0, :]
contour_x_coords = contour_coords[:, 0]
contour_y_coords = contour_coords[:, 1]



#FInd min and max x and y coords
min_x = min(contour_x_coords) + 36.5
max_x = max(contour_x_coords) - 36.5
min_y = min(contour_y_coords) + 36.5
max_y = max(contour_y_coords) - 36.5

def index_to_notation(x, y):
    return chr(x + 97) + str(y + 1)

squares = {}

for x in range(8):
    for y in range(8):
        coords = (min_x + (max_x - min_x) / 8 * x, min_y + (max_y - min_y) / 8 * y)
        #Cut out the image
        cutout = image[int(coords[1]):int(coords[1] + (max_y - min_y - 5) / 8), int(coords[0]):int(coords[0] + (max_x - min_x - 5) / 8)]
        squares[index_to_notation(x, y)] = cutout


# Display the final image
cv2.imshow('Contours', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
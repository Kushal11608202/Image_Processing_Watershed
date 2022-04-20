import cv2
import numpy as np

def neighbourhood(image, x, y):

    # Save the neighbourhood pixel's values in a dictionary
    neighbour_region_numbers = {}

    for i in range(-1, 2):
        for j in range(-1, 2):
            if (i == 0 and j == 0):
                continue
            if (x+i < 0 or y+j < 0): # If coordinates out of image range, skip
                continue
            if (x+i >= image.shape[0] or y+j >= image.shape[1]): # If coordinates out of image range, skip
                continue
            if (neighbour_region_numbers.get(image[x+i][y+j]) == None):
                neighbour_region_numbers[image[x+i][y+j]] = 1 # Create entry in dictionary if not already present
            else:
                neighbour_region_numbers[image[x+i][y+j]] += 1 # Increase count in dictionary if already present

    # Remove the key - 0 if exists
    if (neighbour_region_numbers.get(0) != None):
        del neighbour_region_numbers[0]

    # Get the keys of the dictionary
    keys = list(neighbour_region_numbers)

    # Sort the keys for ease of checking
    keys.sort()

    if (keys[0] == -1):
        if (len(keys) == 1): # Separate region
            return -1
        elif (len(keys) == 2): # Part of another region
            return keys[1]
        else: # Watershed
            return 0
    else:
        if (len(keys) == 1): # Part of another region
            return keys[0]
        else: # Watershed
            return 0

def watershed_segmentation(image):
    # Create a list of pixel intensities along with their coordinates
    intensity_list = []
    for x in range(image.shape[0]):
        for y in range(image.shape[1]):
            # Append the tuple (pixel_intensity, xy-coord) to the end of the list
            intensity_list.append((image[x][y], (x, y)))

    # Sort the list with respect to their pixel intensities, in ascending order
    intensity_list.sort()

    # Create an empty segmented_image numpy ndarray initialized to -1's
    seg_image = np.full(image.shape, -1, dtype = int)

    # Iterate the intensity_list in ascending order and update the segmented image
    region_number = 0

    for i in range(len(intensity_list)):

        # Getting x,y coordinates
        x = intensity_list[i][1][0]
        y = intensity_list[i][1][1]

        # Get the region number of the current pixel's region by checking its neighbouring pixels
        region_status = neighbourhood(seg_image, x, y)

        # Assign region number (or) watershed accordingly, at pixel (x, y) of the segmented image
        if (region_status == -1): # Separate region
            region_number += 1
            seg_image[x][y] = region_number

        elif (region_status == 0): # Watershed
            seg_image[x][y] = 0

        else: # Part of another region
            seg_image[x][y] = region_status

    # Return the segmented image
    return seg_image


# MAIN() :
img = cv2.imread("images/2.png", 0)

WS_image = watershed_segmentation(img)

# Saving the segmented image as output.png to local disk space
cv2.imwrite("images/output.png", WS_image)
watseg_img = cv2.imread("images/output.png", 0)

scale_percent = 30
width = int(img.shape[1] * scale_percent / 100)
height = int(img.shape[0] * scale_percent / 100)
dim = (width*2, height)

original_img = cv2.resize(img, dim)
seg_img = cv2.resize(watseg_img, dim)

cv2.imshow('Original Image : ', original_img)
cv2.imshow('Segmented Image : ', seg_img)
cv2.waitKey(0)

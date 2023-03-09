import cv2
import numpy as np

'''The objective of this program is going to be that we have a bunch of repetitve shots that need to be green screened and replaced with a certain type of background . 
but in certain cases some shots might have some extra green spill than the other so we try to find out the green difference and set a certain threshold for the percentage diff
and if it exceeds above the threshold it supresses the spill and batch renders the shots'''


# Load the images
img1 = cv2.imread('C:/Users/graphic/Desktop/test/control_00000.jpg')
img2 = cv2.imread('C:/Users/graphic/Desktop/test/test_00001.jpg')

#get the absolute difference of the green channel between the two images 
green_diff = np.abs(img1[:,:,1] - img2[:,:,1])

# Threshold the difference to identify areas of significant green spill
green_spill_mask = green_diff > 0.01 

# Count the number of significant green spill pixels and calculate the percentage
num_spill_pixels = np.count_nonzero(green_spill_mask)
total_pixels = img1.shape[0] * img1.shape[1]
percent_spill = num_spill_pixels / total_pixels * 100

# Print the percentage of pixels with significant green spill
print('Green spill:', percent_spill, '%')

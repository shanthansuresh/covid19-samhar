#TODO: Add arg parse functions and documentation

import cv2
import numpy as np
import glob
 
img_array = []
for filename in glob.glob('./*.jpg'):
    img = cv2.imread(filename)
    height, width, layers = img.shape
    size = (width,height)
    img_array.append(img)
 
fourcc = cv2.VideoWriter_fourcc(*'MP4V')
#out = cv2.VideoWriter('project.avi',cv2.VideoWriter_fourcc(*'DIVX'), 5, size)
out = cv2.VideoWriter('crowd.mp4', fourcc, 5, size)
 
for i in range(len(img_array)):
    out.write(img_array[i])
out.release()

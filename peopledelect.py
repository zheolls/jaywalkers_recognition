 # import the necessary packages
from __future__ import print_function
from imutils.object_detection import non_max_suppression
from imutils import paths
import numpy as np
import argparse
import imutils
import cv2
import re
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())


def get_walkers(imagePath):
    framelist=[]
    # load the image and resize it to (1) reduce detection time
    # and (2) improve detection accuracy
    image = cv2.imread(imagePath)
    #image = imutils.resize(image, width=min(400, image.shape[1]))
    orig = image.copy()

    # detect people in the image
    (rects, weights) = hog.detectMultiScale(image, winStride=(4, 4),
        padding=(8, 8), scale=1.05)

     # draw the original bounding boxes
    for (x, y, w, h) in rects:
         cv2.rectangle(orig, (x, y), (x + w, y + h), (0, 0, 255), 2)
    rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
    pick = non_max_suppression(rects, probs=None, overlapThresh=0.55)
    for (xA, yA, xB, yB) in pick:
        cv2.rectangle(image, (xA, yA), (xB, yB), (0, 255, 0), 2)
        framelist.append((xA, yA, xB, yB))
    imagePath=re.sub("images",'output',imagePath)
    imagePath=re.sub(r"\.[a-z]+",'',imagePath)+'_walker'+re.findall(r"\.[a-z]+",imagePath)[0]
    cv2.imwrite(imagePath, image, [int(cv2.IMWRITE_JPEG_QUALITY), 95])  # 默认95
    return framelist
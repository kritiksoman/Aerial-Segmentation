import cv2
import numpy as np
from skimage import measure
from skimage.measure import regionprops

def smooth(roofMask2):
    index,n = measure.label(roofMask2, connectivity=2, return_num=True)
    region = regionprops(index, cache = True)
    number_regions = len(region)
    height,width = roofMask2.shape
    maskBB = []
    maskLabel =[]

    roofnew = np.zeros((height,width))
    for i in range(0,number_regions):
        maskBB.append(region[i].bbox)
        maskLabel.append(region[i].label)
    kernel1 = np.ones((2,2),np.uint8)
    kernel2 = np.ones((2,2),np.uint8)

    for regionIndex in range(0,number_regions):
        minr, minc, maxr, maxc = maskBB[regionIndex]
        extraMargin = 10
        if minr-extraMargin<0:
            minr=0
        else:
            minr=minr-extraMargin
        if minc-extraMargin<0:
            minc=0
        else:
            minc=minc-extraMargin
        if maxr+extraMargin>height:
            maxr=height
        else:
            maxr=maxr+extraMargin
        if maxc+extraMargin>width:
            maxc=width
        else:
            maxc=maxc+extraMargin
        regionbb = index[minr:maxr,minc:maxc]
        mask = (regionbb == maskLabel[regionIndex]).astype(np.uint8)*255
        mask = cv2.dilate(mask,kernel1,iterations = 1)
        mask = cv2.erode(mask,kernel2,iterations = 1)
        if np.sum(mask)!=0: #accumulate result
            roofnew[minr:maxr,minc:maxc]=roofnew[minr:maxr,minc:maxc]+mask    

    return roofnew

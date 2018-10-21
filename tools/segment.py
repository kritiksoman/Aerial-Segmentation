from skimage.feature import canny 
import scipy.ndimage as ndimage
import cv2
import gdal
import numpy as np
from skimage.morphology import skeletonize
from skimage import measure

def segmentDEM(original_dem):
	height,width = original_dem.shape
	fg = original_dem>0


	blurred_f = ndimage.gaussian_filter(original_dem, 6)
	filter_blurred_f = ndimage.gaussian_filter(blurred_f, 1)
	alpha = 20
	x = alpha * (blurred_f - filter_blurred_f)
	blurred_f=filter_blurred_f=None
	sharpened = original_dem + x

	one=cv2.bilateralFilter(sharpened,5,5,5)
	sharpened=None
	cannyEdge = canny(one, sigma=0.15, low_threshold=0.15, high_threshold=1, mask=fg>0)
	one=None
	cannyEdge = cannyEdge>0
	cannyEdge = cannyEdge.astype(np.uint8)*255

	kernel = np.ones((10,10),np.uint8)
	mask2 = cv2.dilate(cannyEdge,kernel,iterations = 1)
	cannyEdge=None
	mask2=mask2>0
	mask2=mask2.astype(np.uint8)
	fg=fg.astype(np.uint8)

	pad = np.ones((height+2,width+2),dtype=np.uint8)
	pad[1:height+1,1:width+1]=mask2
	mask2 = pad
	pad = None 	

	skeleton = 1-skeletonize(mask2)
	mask2=None
	
	index,n = measure.label(skeleton, connectivity=1, return_num=True)
	skeleton=None
	index = index[1:height+1,1:width+1]
	if height*width!=np.sum(fg):
		kernel = np.ones((15,15),np.uint8)
		fg = cv2.erode(fg,kernel,iterations = 1)
		index = np.multiply(index,fg)
	return index,n

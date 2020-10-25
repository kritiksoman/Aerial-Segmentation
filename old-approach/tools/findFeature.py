from skimage.feature import canny 
import scipy.ndimage as ndimage
import cv2
import gdal
import numpy as np
from skimage.morphology import skeletonize
from skimage import measure
from skimage.measure import regionprops
from multiprocessing import pool, cpu_count
from multiprocessing.dummy import Pool as ThreadPool

#define variables
featureList=[]
maxArea=0
xy=[]
areaList = []
indexList =[]
maskBB = []
maskHeight = []
maskLabel = []
maskStd = []
neighbours=0
regionbb=0
mask=0
regionval=0
smallerThan=0
kernel = np.ones((20,20),np.uint8)

def findStdSmaller(regionIndex):
    global smallerThan
    pos = np.where(maskLabel==neighbours[regionIndex])
    mask2 = (regionbb == maskLabel[pos]).astype(np.uint8)*255
    mask2 = cv2.dilate(mask2,kernel,iterations = 1)>0
    mask2 = np.multiply(mask2,mask>0)
    mask2 = np.multiply(mask2,regionval)
    hData = mask2[np.where(mask2>0)]
    if len(hData)>0:
        h = np.mean(hData)
        if h<maskHeight[pos]+2:
            smallerThan=smallerThan+1

def findDEMFeature(original_dem,index):
	global featureList,maxArea,xy,areaList,indexList,maskBB,maskHeight,maskLabel,maskStd,\
		neighbours,regionbb,mask,regionval,smallerThan,kernel
	height,width=original_dem.shape
	region = regionprops(index, original_dem,cache = True)
	number_regions=len(region)
	for i in range(0,number_regions):
	    if region[i].area>10000:
	        areaList.append(region[i].area)
	        indexList.append(i)
	        maskBB.append(region[i].bbox)
	        maskLabel.append(region[i].label)
	        maskHeight.append(region[i].mean_intensity)
	        xy = region[i].coords
	        std = np.std(original_dem[xy[:,0],xy[:,1]])
	        maskStd.append(std)	

	areaList = np.array(areaList)
	indexList = np.array(indexList)
	maskBB = np.array(maskBB)
	maskHeight = np.array(maskHeight)
	maskLabel = np.array(maskLabel)
	maskStd = np.array(maskStd)
	order = np.argsort(-areaList)#minus for decending
	areaList = areaList[order]
	indexList = indexList[order]
	maskBB = maskBB[order]
	maskHeight = maskHeight[order]
	maskLabel = maskLabel[order]
	maskStd = maskStd[order]

	for regionIndex in range(0,len(areaList)):
	    minr, minc, maxr, maxc = maskBB[regionIndex]
	    extraMargin = 20
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
	    contours = cv2.findContours(mask, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)[1]

	    holeData = []
	    if len(contours)-1>0:
	        for j in range(0,len(contours)-1):
	            cnt = contours[j+1]
	            pos = cnt[0]
	            area = cv2.contourArea(cnt)
	            if area>1000:
	                holeData.append(cv2.contourArea(contours[j+1]))
	        if len(holeData)>0:
	            number_holes = len(holeData)
	            holeData = np.sort(holeData)
	            avgHole = np.mean(holeData,dtype=np.int)
	        else:
	            number_holes = avgHole = largestHole = 0

	    else:
	        number_holes = avgHole = largestHole = 0


	    cnt = contours[0]
	    hull = cv2.convexHull(cnt,returnPoints = False)
	    defects = cv2.convexityDefects(cnt,hull)
	    defectData=[]
	    if defects is not None:
	        total_number_defects=len(defects)
	        for i in range(defects.shape[0]):
	            d = defects[i,0][3]
	            if d>100000:
	                defectData.append(d)
	        if len(defectData)>0:
	            number_defects = len(defectData)
	            defectData = np.sort(defectData)
	            avgDefect = np.mean(defectData,dtype=np.int)
	        else:
	            number_defects = avgDefect = 0
	    else:
	            number_defects = avgDefect = 0
	            total_number_defects=0
	 
	    mask2 = cv2.dilate(mask,kernel,iterations = 1)>0
	    regionbb = np.multiply(mask2,regionbb)
	    neighbours = np.unique(regionbb)
	    if neighbours[0]==0:
	        neighbours=neighbours[1:-1]
	    removePos = np.where(neighbours==maskLabel[regionIndex])
	    neighbours = np.delete(neighbours,removePos)

	    neighbours = np.intersect1d(neighbours,maskLabel)#to take only large area adjacent segments
	    smallerThan = 0

	    if maskStd[regionIndex]>2:
	        regionval = original_dem[minr:maxr,minc:maxc]
	        pool = ThreadPool(int(cpu_count()))
	        pool.map(findStdSmaller,range(0,len(neighbours)))
	        pool.close()
	        pool.join()
	    else:
	        for i in range(0,len(indexList)):
	            for j in range(0,len(neighbours)):
	                if maskLabel[i]==neighbours[j]:
	                    if maskHeight[i]>maskHeight[regionIndex]+2:
	                        smallerThan=smallerThan+1

	    featureList.append([maskLabel[regionIndex],number_holes,avgHole,\
	    	number_defects,total_number_defects,smallerThan,int(np.ceil(maskStd[regionIndex]))])

	return np.array(featureList),region

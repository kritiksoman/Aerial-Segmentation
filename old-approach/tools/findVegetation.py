from __future__ import division
import gdal
import numpy as np
import cv2
from skimage.measure import regionprops

def NDVI(location,FileName,original_ortho):
	File = gdal.Open(location+FileName)
	NIR = File.GetRasterBand(1)
	NIR = NIR.ReadAsArray()
	a=np.subtract(NIR,original_ortho[:,:,0],dtype=np.int)
	b=np.add(NIR,original_ortho[:,:,0],dtype=np.int)
	NDVI=np.divide(a, b,dtype=np.float)
	NDVI=NDVI>0.1
	NDVI=NDVI.astype(np.uint8)*255
	return NDVI

def LABThreshold(original_ortho):
	lab = cv2.cvtColor(original_ortho, cv2.COLOR_RGB2Lab)
	lower_range = np.array([0,102,117], dtype=np.uint8)
	upper_range = np.array([218,127,225], dtype=np.uint8)
	greenMask = cv2.inRange(lab, lower_range, upper_range)
	greenMask = greenMask.astype(np.uint8)*255
	return greenMask

def removeLABRoof(roofMask,original_ortho,index,region):
	roofMask2 = np.copy(roofMask)
	vegetation = LABThreshold(original_ortho)>0
	vegetation2 = np.multiply(index,vegetation)

	regionVege = regionprops(vegetation2)
	regionVegeLabel = []
	regionVegeArea = []
	for i in range(0,len(regionVege)):
		regionVegeLabel.append(regionVege[i].label)
		regionVegeArea.append(regionVege[i].area)
	regionVegeArea = np.array(regionVegeArea)

	regionLabel = []
	regionArea = []
	#order = []
	for i in range(0,len(region)):
		currLabel = region[i].label
		if currLabel in regionVegeLabel:
			regionLabel.append(currLabel)
			regionArea.append(region[i].area)
	regionLabel = np.array(regionLabel)
	regionArea = np.array(regionArea)
	areaRatio = regionVegeArea/regionArea
	vegeMask = np.zeros(index.shape,dtype=np.uint8)
	removeRegions = regionLabel[np.where(areaRatio>0.5)]
	for r in region:
		if r.label in removeRegions and r.area<20000:
			xy=r.coords
			roofMask2[xy[:,0],xy[:,1]]=0
			vegeMask[xy[:,0],xy[:,1]]=100	

	return roofMask2,vegeMask,vegetation

def removeNDVIRoof(location,FileName,roofMask,original_ortho,index,region):
	roofMask2 = np.copy(roofMask)
	vegetation = NDVI(location,FileName,original_ortho)>0
	vegetation2 = np.multiply(index,vegetation)

	regionVege = regionprops(vegetation2)
	regionVegeLabel = []
	regionVegeArea = []
	for i in range(0,len(regionVege)):
		regionVegeLabel.append(regionVege[i].label)
		regionVegeArea.append(regionVege[i].area)
	regionVegeArea = np.array(regionVegeArea)

	regionLabel = []
	regionArea = []
	for i in range(0,len(region)):
		currLabel = region[i].label
		if currLabel in regionVegeLabel:
			regionLabel.append(currLabel)
			regionArea.append(region[i].area)
	regionLabel = np.array(regionLabel)
	regionArea = np.array(regionArea)
	areaRatio = regionVegeArea/regionArea
	vegeMask = np.zeros(index.shape,dtype=np.uint8)
	removeRegions = regionLabel[np.where(areaRatio>0.5)]
	for r in region:
		if r.label in removeRegions and r.area<20000:
			xy=r.coords
			roofMask2[xy[:,0],xy[:,1]]=0
			vegeMask[xy[:,0],xy[:,1]]=100	

	return roofMask2,vegeMask,vegetation

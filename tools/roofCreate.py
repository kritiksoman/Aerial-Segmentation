from __future__ import division
import numpy as np
from multiprocessing import pool, cpu_count
from multiprocessing.dummy import Pool as ThreadPool
import cv2

gHeight = []
Height = []
Index = []
Pos = []
maskBB = []
maskLabel = []
pBuilding = []
pGround = []

update = 0
updateold = 0
nochange = 0

def createMask(original_dem,index,groundMask,region,groundLabel,gListStd,minBuildingHeight):
    global Height,Index,Pos,maskBB,remaining,maskLabel,update,updateold,nochange
    height,width = index.shape
    for i in range(0,len(region)):
        if region[i].label  in groundLabel:
            gHeight.append(region[i].mean_intensity)
        else:
            Height.append(region[i].mean_intensity)
            Index.append(i)
            Pos.append(region[i].coords)
            maskBB.append(region[i].bbox)
            maskLabel.append(region[i].label)

    roofMask = np.zeros((height,width),dtype=np.uint8)
    kernel1 = np.ones((5,5),dtype=np.uint8)
    kernel2 = np.ones((10,10),dtype=np.uint8)

    def fillMask(regionIndex):
        global pBuilding,pGround,update
        minr, minc, maxr, maxc = maskBB[regionIndex]

        extraMargin = 205
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
        regionval = original_dem[minr:maxr,minc:maxc]

        neighbours = np.unique(regionbb)
        if neighbours[0]==0:
            neighbours=neighbours[1:]
        h = 0
        g = np.intersect1d(neighbours,groundLabel)
        if len(g)>0:
            loc = np.where(g[0]==groundLabel)[0]
            if gListStd[loc[0]]>1:
                gRegion1 = regionbb==g[0]
                gRegion2 = gRegion1.astype(np.uint8)*255
                gRegion2 = cv2.erode(gRegion2,kernel1,iterations = 1)
                gRegion3 = cv2.erode(gRegion2,kernel1,iterations = 1)>0
                gRegion2 = gRegion2>0
                boundaryRegion = np.multiply(gRegion2,1-gRegion3)
                if np.sum(boundaryRegion)==0:#ground region is not in boundary
                    gRegion1 = gRegion1.astype(np.uint8)
                    h=np.sum(np.multiply(gRegion1,regionval))/np.sum(gRegion1)
                    
                else:
                    h=np.sum(np.multiply(boundaryRegion,regionval))/np.sum(boundaryRegion)
                    
            else:
                h = gHeight[loc[0]]

            if Height[regionIndex]>h+minBuildingHeight:
                xy=Pos[regionIndex]
                roofMask[xy[:,0],xy[:,1]]=255
                pBuilding.append(maskLabel[regionIndex])
                pGround.append(h)
                
                update = update + 1
            remaining.remove(regionIndex)
            
        else:
             c = np.intersect1d(neighbours,pBuilding)
             if len(c)>0:
                locc = np.where(c[0]==pBuilding)[0]
                h = pGround[locc[0]]
                if Height[regionIndex]>h+minBuildingHeight:
                    xy=Pos[regionIndex]
                    roofMask[xy[:,0],xy[:,1]]=255

                    pBuilding.append(maskLabel[regionIndex])
                    pGround.append(h)
                    
                    update = update + 1
                remaining.remove(regionIndex)
        
    remaining = list(range(0,len(Index)))#list() added for python 3

    while True:
        if len(remaining)>0:
            
            pool = ThreadPool(cpu_count())
            pool.map(fillMask,remaining)
            pool.close()
            pool.join()                            

        else:
            break
        if update-updateold==0:
            nochange=nochange+1
        if nochange==2:
            break
        updateold=update

    return roofMask


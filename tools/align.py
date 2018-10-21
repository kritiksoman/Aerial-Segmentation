#align DEM and ortho

from __future__ import division
import gdal
import numpy as np
import numpy.linalg as la
import matplotlib.patches as mpatches
from skimage.measure import regionprops
import os 

# funtion to covert row,col of one tiff to another
def pixToGeoToPix(x1_index, y1_index, gt1, gt2):
    # x1_index: x index of pixel in first image
    # y1_index: y index of pixel in first image
    # gt1: geotransform tuple of first image
    # gt2: geotransform tuple of second image
    geo_x = gt1[0] + gt1[1]*x1_index
    geo_y = gt1[3] + gt1[5]*y1_index
    x2_index = int((geo_x-gt2[0])/gt2[1])
    y2_index = int((-gt2[3]+geo_y)/gt2[5])
    return x2_index, y2_index

# funtion to covert row,col to lat,lon
# def togeo(x1_index, y1_index, gt1):
#     geo_x = gt1[0] + gt1[1]*x1_index
#     geo_y = gt1[3] + gt1[5]*y1_index
#     return geo_x, geo_y

def DEMOrthoAlign(locationDEM,locationOrtho,demFileName,orthoFileName):
    original_dem = gdal.Open(locationDEM+demFileName)
    xmax=original_dem.RasterXSize
    ymax=original_dem.RasterYSize
    gtDem = original_dem.GetGeoTransform()
    wkt = original_dem.GetProjection()
    img1_dem = original_dem.GetRasterBand(1).ReadAsArray()
    original_dem_fg = img1_dem>0
    original_dem_fg = original_dem_fg.astype(np.uint8)
    region = regionprops(original_dem_fg)
    img1_dem = np.multiply(img1_dem,original_dem_fg)
    original_dem_fg = None
    minr_dem, minc_dem, maxr_dem, maxc_dem = region[0].bbox
    height_dem = maxr_dem-minr_dem
    width_dem = maxc_dem-minc_dem
    demArea = (height_dem) * (width_dem)

    ortho=locationOrtho+orthoFileName
    orthoHandle = gdal.Open(ortho)
    gtOrtho = orthoHandle.GetGeoTransform()
    if (gtOrtho[1]==gtDem[1]) and (gtOrtho[5]==gtDem[5]):#if pixel size match already
        orthoPixelMatch=orthoHandle
        orthoHandle=None
    else:#create a tiff file which has same pixel size as DEM
        orthoPixelMatchFileName=orthoFileName+"PixelMatch.tif"
        if os.path.isfile(locationOrtho+orthoPixelMatchFileName):
            orthoPixelMatch = gdal.Open(locationOrtho+orthoPixelMatchFileName)
        else:
            orthoPixelMatch = gdal.Warp(locationOrtho+orthoPixelMatchFileName, ortho, targetAlignedPixels = True, xRes=np.absolute(gtDem[1]), yRes=np.absolute(gtDem[5]))

    #load ortho
    xmax=orthoPixelMatch.RasterXSize
    ymax=orthoPixelMatch.RasterYSize
    gtOrtho = orthoPixelMatch.GetGeoTransform()

    bnd1_ortho = orthoPixelMatch.GetRasterBand(1)
    img1_ortho = bnd1_ortho.ReadAsArray(0,0,xmax,ymax)
    bnd1_ortho = None
    bnd2_ortho = orthoPixelMatch.GetRasterBand(2)
    img2_ortho = bnd2_ortho.ReadAsArray(0,0,xmax,ymax)
    bnd2_ortho = None
    bnd3_ortho = orthoPixelMatch.GetRasterBand(3)
    img3_ortho = bnd3_ortho.ReadAsArray(0,0,xmax,ymax)
    bnd3_ortho = None

    
    if orthoPixelMatch.RasterCount==4:
        bnd4_ortho = orthoPixelMatch.GetRasterBand(4)
        original_ortho_fg = bnd4_ortho.ReadAsArray(0,0,xmax,ymax)>0
        bnd4_ortho = None
    else:
        original_ortho_fg=np.multiply(img1_ortho>-1,img2_ortho>-1,img3_ortho>-1)

    img = np.dstack((img1_ortho,img2_ortho,img3_ortho))
    img1_ortho = img2_ortho = img3_ortho = None


    original_ortho_fg = original_ortho_fg.astype(np.uint8)
    region = regionprops(original_ortho_fg)
    minr_ortho, minc_ortho, maxr_ortho, maxc_ortho = region[0].bbox
    height_ortho = maxr_ortho-minr_ortho
    width_ortho = maxc_ortho-minc_ortho
    orthoArea = (height_ortho) * (width_ortho)


    if orthoArea<=demArea:
        minc_ref, minr_ref = pixToGeoToPix(minc_ortho,minr_ortho,gtOrtho,gtDem)
        maxc_ref, maxr_ref = pixToGeoToPix(maxc_ortho,maxr_ortho,gtOrtho,gtDem)
        original_ortho = img[minr_ortho:maxr_ortho,minc_ortho:maxc_ortho,:]
        original_dem = img1_dem[minr_ref:maxr_ref,minc_ref:maxc_ref]
        gtRef = gtDem        
        
    else:
        minc_ref, minr_ref = pixToGeoToPix(minc_dem,minr_dem,gtDem,gtOrtho)
        maxc_ref, maxr_ref = pixToGeoToPix(maxc_dem,maxr_dem,gtDem,gtOrtho)
        original_dem = img1_dem[minr_dem:maxr_dem,minc_dem:maxc_dem]
        original_ortho = img[minr_ref:maxr_ref,minc_ref:maxc_ref,:]
        gtRef = gtOrtho

    img1_dem = img = gtOrtho = gtDem = None
    height, width = original_dem.shape


    return original_dem,original_ortho,[gtRef,minc_ref,minr_ref,wkt]

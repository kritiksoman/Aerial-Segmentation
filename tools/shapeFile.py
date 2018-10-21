import osgeo.ogr, osgeo.osr #we will need some packages
from osgeo import ogr #and one more for the creation of a new field
import cv2
import numpy as np
from skimage import measure
from skimage.measure import regionprops
from multiprocessing import pool, cpu_count
from multiprocessing.dummy import Pool as ThreadPool

def createShapeFile(roofnew,FileName,coordRef,approximate):
    height,width = roofnew.shape
    [gtRef,c_offset,r_offset,wkt] = coordRef

    def create_polygon(x):
        poly = ogr.Geometry(ogr.wkbPolygon)# Create polygon
        for i in range(0,len(x)):
            if i==0:
                outRing = ogr.Geometry(ogr.wkbLinearRing)
                coords=x[0]
                for coord in coords:
                    outRing.AddPoint(coord[0], coord[1])
                poly.AddGeometry(outRing)
            else:
                innerRing=ogr.Geometry(ogr.wkbLinearRing)
                coords=x[i]
                for coord in coords:
                    innerRing.AddPoint(coord[0], coord[1])
                poly.AddGeometry(innerRing)
        return poly.ExportToWkt()

    def convertCoord(padfTransform,indices):
        a=indices[0]+c_offset
        b=indices[1]+r_offset
        xp = padfTransform[0] + a*padfTransform[1] + a*padfTransform[2]
        yp = padfTransform[3] + b*padfTransform[4] + b*padfTransform[5]
        return xp,yp

    class buildingRoof:#class to store building number, coordinates, and area flag
      areaFlag=-1
      bNum=-1
      coords=[]

    def collect_boundary(regionIndex):
        edge=[]
        minr, minc, maxr, maxc = maskBB[regionIndex]
        extraMargin = 5
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
        regionbb = roofnew[minr:maxr,minc:maxc]
        mask = (regionbb == maskLabel[regionIndex]).astype(np.uint8)*255
        im, contoursTotal,hierarchyTotal = cv2.findContours(mask, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        if len(contoursTotal)>0:
            hierarchyTotal=hierarchyTotal[0]
            for a in range(0,len(contoursTotal)):
                #find boundary points
                hierarchy=hierarchyTotal[a]
                cnt=contoursTotal[a]
                if approximate == 1:
                    epsilon = 0.01*cv2.arcLength(cnt,True)
                    if epsilon>10:#max epsilon value is 10
                        epsilon=10
                    approx = cv2.approxPolyDP(cnt,epsilon,True)
                else:
                    approx = cnt
                bpoints=[]
                for xy in approx:
                    bpoints.append([xy[0,0]+minc,xy[0,1]+minr])
                #print np.asarray(bpoints)
                b=buildingRoof()
                if hierarchy[3]<0: #if no parent
                    b.areaFlag=1
                elif hierarchy[2]<0: #if no child
                    b.areaFlag=0
                b.bNum=regionIndex
                b.coords=np.asarray(bpoints)
                edge.append(b)
            bs.append(edge)

    def create_shape_file(i):
        edges=bs[i]
        x=[]
        #print(len(edges))
        for j in range(0,len(edges)):
            b=edges[j]
            y=[]
            for k in range(0,len(b.coords)):
                y.append(convertCoord(gtRef,b.coords[k]))
            y.append(convertCoord(gtRef,b.coords[0]))#first and
            x.append(y)
        poly = create_polygon(x)
        featureIndex = b.bNum #this will be the first point in our dataset
        feature = osgeo.ogr.Feature(layer_defn)
        feature.SetField('id', featureIndex)
        geom = osgeo.ogr.CreateGeometryFromWkt(poly)
        feature.SetGeometry(geom)
        layer.CreateFeature(feature)
        feature = geom = None  # destroy these

    bs = []
    roofnew=roofnew>0

    roofnew,number_regions = measure.label(roofnew, connectivity=1, return_num=True)

    region = regionprops(roofnew, cache = True)
    maskBB = []
    maskLabel = []
    for i in range(0,number_regions):
        maskBB.append(region[i].bbox)
        maskLabel.append(region[i].label)

    pool = ThreadPool(cpu_count())
    pool.map(collect_boundary,range(0,number_regions))
    pool.close()
    pool.join()


    #create shape File
    path="roof_" + FileName + ".shp"
    spatialReference = osgeo.osr.SpatialReference() #will create a spatial reference locally to tell the system what the reference will be
    spatialReference.ImportFromWkt(wkt)
    driver = osgeo.ogr.GetDriverByName('ESRI Shapefile') # will select the driver foir our shp-file creation.
    shapeData = driver.CreateDataSource(path) #so there we will store our data
    layer = shapeData.CreateLayer('customs', spatialReference, osgeo.ogr.wkbPolygon) #this will create a corresponding layer for our data with given spatial information.
    layer_defn = layer.GetLayerDefn() # gets parameters of the current shapefile
    layer.CreateField(ogr.FieldDefn('id', ogr.OFTInteger))

    pool = ThreadPool(cpu_count())
    pool.map(create_shape_file,range(0,len(bs)))
    pool.close()
    pool.join()
    ds = layer = feat = geom = None
    shapeData.Destroy()# Save and close everything

    

# Rooftop Detection Algorithm

[![MIT](https://img.shields.io/badge/license-MIT-brightgreen.svg)](https://github.com/kritiksoman/Rooftop-Segmentation/blob/master/LICENSE)

## Overview
This is the python code for detecting rooftops from Aerial RGBD (and IR if available) data using simple image processing techniques. It uses moderate computational resources and has low interface time for segmenting rooftops. Works best on elevation data generated from photogrammetry with around 5cm ground resolution. The two inputs are the RGB (ortho-photo) and the Digital Elevation Model (DEM) geotifs. IR band data may be additionally provided for using NDVI in removing tree canopies more accurately. The shape files for the roofs and clutter in roof are generated as output which can be opened in any GIS software like [QGIS](https://qgis.org/en/site/).

This work has been accepted for publication in ACM India Joint International Conference on Data Science and Management of Data ([CoDS-COMAD 2019](http://cods-comad.in/2019/index.html)).

## Dependencies
```
cv2
gdal
scipy
skimage
matplotlib
numpy
multiprocessing
osgeo
```
## Usage
```
python roofSegmentAlgo.py
```

## Result Screenshots
[1] Rooftop segmentation and clutter <br/>

| DEM consisting of rooftops| Ortho-photo of rooftops| The detected rooftops along with clutter|
| ------------- |:-------------:| -----:|
|![image1](https://github.com/kritiksoman/Rooftop-Segmentation/blob/master/results/DEM.png)| ![image2](https://github.com/kritiksoman/Rooftop-Segmentation/blob/master/results/Ortho.png) | ![image3](https://github.com/kritiksoman/Rooftop-Segmentation/blob/master/results/Roof_n_clutter.png) |

[2] DEM Segmentation <br/>
![image4](https://github.com/kritiksoman/Rooftop-Segmentation/blob/master/results/segmentedDEM.png)

[3] Rooftop segmentation when roof is covered with grass <br/>

| Ortho-photo| Segmented rooftops|
| ------------- |:-------------:| 
|![image1](https://github.com/kritiksoman/Rooftop-Segmentation/blob/master/results/g1.png)| ![image2](https://github.com/kritiksoman/Rooftop-Segmentation/blob/master/results/g2.png) |

## Author
Kritik Soman

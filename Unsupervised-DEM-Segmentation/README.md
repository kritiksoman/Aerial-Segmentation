# Unsupervised DEM Segmentation
IPython Notebook showing simple segmentation of aerial Digital Elevation Model (DEM) data.

[![MIT](https://img.shields.io/badge/license-MIT-brightgreen.svg)](https://github.com/kritiksoman/Aerial-Segmentation/blob/master/Unsupervised-DEM-Segmentation/LICENSE)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kritiksoman//Aerial-Segmentation/blob/master/Unsupervised-DEM-Segmentation/Unsupervised_DEM_Segmentation.ipynb)


## Overview
The notebook shows how DEM can be segmented by using basic image processing techniques. It uses the method described in https://doi.org/10.1145/3297001.3297041 .
This method works because rooftop edges are mostly step edges.


## Dependencies
```
cv2 
gdal
scipy
skimage
matplotlib
numpy
```

## Result Screenshot
![image1](https://github.com/kritiksoman/Aerial-Segmentation/blob/master/Unsupervised-DEM-Segmentation/results/DEM_Segment.png)

## How to run: 
[1] Download the sample file: 'DEM.tif'<br/>
[2] Click on 'Open in Colab' and upload the above file.<br/>
[3] Run cells in notebook.<br/>

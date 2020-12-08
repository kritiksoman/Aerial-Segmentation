# Rooftop Detection Algorithm

[![MIT](https://img.shields.io/badge/license-MIT-brightgreen.svg)](https://github.com/kritiksoman/Rooftop-Segmentation/blob/master/LICENSE)

## Overview
This is the python code for detecting rooftops from Aerial RGBD (and IR if available) data using simple image processing techniques. It uses moderate computational resources and has low interface time for segmenting rooftops. Works best on elevation data generated from photogrammetry with around 5cm ground resolution. The two inputs are the RGB (ortho-photo) and the Digital Elevation Model (DEM) geotifs. IR band data may be additionally provided for using NDVI in removing tree canopies more accurately. The shape files for the roofs and clutter in roof are generated as output which can be opened in any GIS software like [QGIS](https://qgis.org/en/site/).<br/>
Why this works?<br/>
[1] No viewpoint variations.<br/>
[2] Scale variation: Ground resolution is already known. (5cm/px in this example)<br/>
[3] No deformation in shape of object segmented. (Building images don't deform like the images of a cat)<br/>
[4] Minimal Occulusion: Only trees cover certain rooftops. (Since we are interested in solar panel deployment, this doesn't matter)<br/>
[5] Illumination variation: We use DEM for segmentation and NIR for detecting vegetation. Other than that, drone data is generally recorded in ideal environmental conditions.<br/>  

## Reference
[[CoDS-COMAD '19](http://cods-comad.in/2019/index.html)]: Soman, Kritik. "[Rooftop Detection using Aerial Drone Imagery](https://dlnext.acm.org/doi/abs/10.1145/3297001.3297041)." Proceedings of the ACM India Joint International Conference on Data Science and Management of Data. 2019.

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
## How to run on Colab?
[1] Download the repository zip and upload on Colab.<br/>
[2] Unzip using the command```! unzip Rooftop-Segmentation.zip```<br/>
[3] Open demo.ipynb, change directory using ```% cd Rooftop-Segmentation``` and run cells.


## Result Screenshots
[1] Rooftop segmentation<br/>

| Our Dataset | ISPRS Potsdam Dataset|
| ------------- |:-------------:| 
|![image1](https://github.com/kritiksoman/Rooftop-Segmentation/blob/master/old-approach/results/Rooftop_1.png)| ![image2](https://github.com/kritiksoman/Rooftop-Segmentation/blob/master/old-approach/results/Rooftop_2.png) |

[2] Clutter and Rooftop segmentation<br/>

| DEM consisting of rooftops| Ortho-photo of rooftops| The detected rooftops along with clutter|
| ------------- |:-------------:| -----:|
|![image1](https://github.com/kritiksoman/Rooftop-Segmentation/blob/master/old-approach/results/DEM.png)| ![image2](https://github.com/kritiksoman/Rooftop-Segmentation/blob/master/old-approach/results/Ortho.png) | ![image3](https://github.com/kritiksoman/Rooftop-Segmentation/blob/master/old-approach/results/Roof_n_clutter.png) |

[3] DEM Segmentation <br/>
![image4](https://github.com/kritiksoman/Rooftop-Segmentation/blob/master/old-approach/results/segmentedDEM.png)

[4] Rooftop segmentation when roof is covered with grass <br/>

| Ortho-photo| Segmented rooftops|
| ------------- |:-------------:| 
|![image1](https://github.com/kritiksoman/Rooftop-Segmentation/blob/master/old-approach/results/g1.png)| ![image2](https://github.com/kritiksoman/Rooftop-Segmentation/blob/master/old-approach/results/g2.png) |

## Poster 
[Project Poster](https://github.com/kritiksoman/Aerial-Segmentation/blob/master/old-approach/Poster.pdf "Project Poster PDF")

## Note
This code was tested with following version of packages:
```
cv2 3.3.0
gdal 2.1.3                    
scipy 0.19.1  
skimage 0.13.0  
matplotlib 2.1.1   
numpy 1.13.3 
```
# Citation
Please cite using the following bibtex entry:
```
@inproceedings{soman2019rooftop,
  title={Rooftop Detection using Aerial Drone Imagery},
  author={Soman, Kritik},
  booktitle={Proceedings of the ACM India Joint International Conference on Data Science and Management of Data},
  pages={281--284},
  year={2019}
}

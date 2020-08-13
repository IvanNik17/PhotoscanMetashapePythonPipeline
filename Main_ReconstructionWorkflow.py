# -*- coding: utf-8 -*-
"""
Created on Fri Dec 14 08:42:16 2018

@author: ivan
"""

import os 
import numpy as np

import subprocess
from slicePointCloud_v1 import slicer_v1 #The slicing script which cuts the 3D point cloud into 2D* parts

from ScalePaper_realDataV2 import scaleAndUncertanty


# Function which executes the subprocess running on Photoscan. This is done so the python code can be used directly,
# without the need to start it from the Photoscan

def execute(cmd):
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line 
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)

# Name of the Photoscan exe, change only if renaming the exe
photoscanName = "photoscan.exe"

# Directory where Photoscan has been installed on the computer. You need the Pro version of the program
photoscanDir=r"...\Agisoft\PhotoScan Pro"

# Directory where the slave code is put. The slave code is the one that runs on Photoscan and creates the point cloud, normals and colors
codeDir=r"PhotoscanProcessing_slave.py"

# Check if the Photoscan directory exists and move the run directory to that directory
assert os.path.isdir(photoscanDir)
os.chdir(photoscanDir)

# Directory of the blade photos
image_folder = r"images"


# Directory of the created slices
save_folder=r"slices"

# Name of the coordinate reference file, IF THERE IS NO REFERENCE FILE WRITE - "noRef" instead
coordReference = "coords.txt"
outputPointCloud = "testBlade"


# Add 0 if you don't want to have any limit. Keypoints are the detected features in each image, Tiepoints are the keypoints found on multiple images     
keypointLimit = 80000
tiepointLimit = 80000



# Add 0 for no filter. The first filter removes points with reprojection error more than a specific value (0.3 to 0.5 normal values), 
# The second filter removes points found in a number of images lower than the value (2 or 3 normal value)
# The third filter removes points with reconstruction uncertainty higher than the value (35 to 10 normal values)
    
filterReprojectionError_thresh = 0.3
filterImageCount_thresh = 2
filterReconstructionUncertainty_thresh = 15

# Add 0 for no decimation. Decimate the mesh to a specific vertex count
decimateMesh_size = 1000000


# Accuracy of the alignment and point cloud creation phase. For more information on the different options look at the documentation of PhotoscanProcessing_slave.py
alignAccuracy = 'A_high'
pcAccuracy = 'PC_medium'


# Transform all vlaues to strings
key_str = str(keypointLimit)
tie_str = str(tiepointLimit)
filter_1_str = str(filterReprojectionError_thresh)
filter_2_str = str(filterImageCount_thresh)
filter_3_str = str(filterReconstructionUncertainty_thresh)
size_str = str(decimateMesh_size)


# Execute the slave process on Photoscan as a subprocess and return and print all the console outputs. (line) contains the current output line
for line in execute([photoscanName, "-r", codeDir,image_folder,coordReference,outputPointCloud,key_str,tie_str,filter_1_str,filter_2_str,filter_3_str,size_str,alignAccuracy,pcAccuracy]):
    print(line, end="")
    


# Fix scale of model if needed, plus get the uncertainty of the scale
cams_file = image_folder + "\\" + outputPointCloud + "_cams.txt"

realPos_file = image_folder + "\\" + "coords_noNames.txt"; 

recPoints = np.loadtxt(cams_file, delimiter=',')
    
groundPoints = np.loadtxt(realPos_file, delimiter=' ')

#  change to the sensor uncertainty used to find the ground points
stdDev = [0.017538494, 0.02445698]  

[scale, scaleUncertainty] = scaleAndUncertanty(groundPoints, recPoints, stdDev)



# Check if the save directory for the slices exists, if it does not create it    
if not os.path.exists(save_folder):
    print("Creating Dir")
    os.makedirs(save_folder)
else:
    print("Exists")

# Open the saved pointCloud and load it into this python kernel.    
pointCloud_name = image_folder + "\\" + outputPointCloud + ".txt"    
if 'pointCloud' not in  locals():
        pointCloud = np.loadtxt(pointCloud_name, delimiter = ",")
    
# Remove color information, as it is not needed for now
pointCloud_verts = pointCloud[:,:3]

pointCloud_verts *=scale

# Slice the point cloud and save in the save directory as separate files.
axisSliced = 1

slicer_v1(pointCloud_verts,save_folder,axisSliced,visualization = "2D")   

print("Slicing Ended") 



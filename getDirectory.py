# -*- coding: utf-8 -*-
"""
Created on Tue Sep 18 13:02:28 2018

@author: ivan
"""

import os
import pathlib

from PIL import Image
from PIL.ExifTags import TAGS

import datetime
import time

import numpy as np
import cv2

#
#
#
#
#for file in os.listdir("G:/DCIM/100EOS5D"):
#    if file.endswith(".JPG"):
#        print(os.path.join("/mydir", file))
        
        
        
import win32api

drives = win32api.GetLogicalDriveStrings()
drives = drives.split('\000')[:-1]

sdDrive = ""
dataDrive = ""

for i in range(len(drives)):
    driveLetter = drives[i]
    try:
        
        driverName = win32api.GetVolumeInformation(driveLetter)
        if driverName[0] == "EOS_DIGITAL":
            sdDrive = driveLetter
            print (driverName[0])
        
        if driverName[0] == "DATA":
            dataDrive = driveLetter
        
    except:
        print("error")
        

print("----------------")

imagePaths = []
        
for root, dirs, files in os.walk(sdDrive):
    for file in files:
        if file.endswith(".JPG"):
             imagePaths.append(os.path.join(root, file))
#             print(os.path.join(root, file))

print("Get image paths")
print("----------------")



#Get current image
dateTime_prev = ""
epoch_prev = 0

counter = 0

for i in range(0,len(imagePaths)):

    img = Image.open(imagePaths[i])
    
    
    # Read exif data
    ret = {}
    info = img._getexif()
    
    
    for tag, value in info.items():
        decoded = TAGS.get(tag, tag)
        ret[decoded] = value
    
    #Save the date/time
    
    dateTime_curr = ret.get("DateTimeOriginal")
    
    #Calculate current epoch of image
    
    epoch_curr = time.mktime(datetime.datetime.strptime(dateTime_curr, "%Y:%m:%d %H:%M:%S").timetuple())
    
    if epoch_curr - epoch_prev > 300:
        saveDateTime = dateTime_curr
        saveDateTime = saveDateTime.replace(':', '-')
        savePath = dataDrive + "\\ReconstructionPipeline\\images_" + saveDateTime
        pathlib.Path(savePath).mkdir(parents=True, exist_ok=True) 
        counter = 0
        print("Make new save directory")
     
        
    imagePath = savePath + "\\image_" + str(counter) + ".JPG"
    currFile = pathlib.Path(imagePath)
    
    if currFile.is_file():
        print("exists")
    else:
        img.save(imagePath)
    
    
    
    dateTime_prev = dateTime_curr
    epoch_prev = epoch_curr 
    
    counter +=1


print("All images saved")
print("----------------")
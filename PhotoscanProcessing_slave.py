# -*- coding: utf-8 -*-
"""
Created on Fri Dec 14 08:50:25 2018

@author: ivan
"""

import numpy as np
import PhotoScan
import os,re
import sys

# get the photo (.JPG) list in specified folder. Change the pattern to search for PNG, RAW, etc.
# Append the names to the photoList
def getPhotoList(root_path, photoList):
    pattern = '.JPG$'
    for root, dirs, files in os.walk(root_path):
        for name in files:
            if re.search(pattern,name, re.IGNORECASE):
                cur_path = os.path.join(root, name)
                photoList.append(cur_path)
                
# Switcher function for the alignment accuracy. Depending on the data sent from the main function select the proper accuracy
# Lowest and low are good for initial testing. High is the one that should be used normally. Highest sometimes gives better results but it's
# suseptable to image noise and takes a lot of time
def alignSwitcher(argument):
    switcher = {
        "A_lowest": PhotoScan.LowestAccuracy,
        "A_low": PhotoScan.LowAccuracy,
        "A_medium": PhotoScan.MediumAccuracy,
        "A_high": PhotoScan.HighAccuracy,
        "A_highest": PhotoScan.HighestAccuracy
        
    }

    return switcher.get(argument, PhotoScan.MediumAccuracy)

# Switcher function for the quality of the dense point cloud. The same as the explanation for the alignment accuracy, but here UltraQuality takes even more time 
def densePCSwitcher(argument):
    switcher = {
        "PC_lowest": PhotoScan.LowestQuality,
        "PC_low": PhotoScan.LowQuality,
        "PC_medium": PhotoScan.MediumQuality,
        "PC_high": PhotoScan.HighQuality,
        "PC_ultra": PhotoScan.UltraQuality
        
    }

    return switcher.get(argument, PhotoScan.MediumQuality)
                
# Function used for calculating the normalized normals of the mesh
def normalize_v3(arr):
    ''' Normalize a numpy array of 3 component vectors shape=(n,3) '''
    lens = np.sqrt( arr[:,0]**2 + arr[:,1]**2 + arr[:,2]**2 )
    arr[:,0] /= lens
    arr[:,1] /= lens
    arr[:,2] /= lens                
    return arr

# Main function for headless 3D reconstruction using Photoscan            
def photoscanProcess(root_path, coordReference, outputPointCloud, alignAccuracy, keypointLimit, tiepointLimit, denseCloudQuality, 
                     filterReprojectionError_thresh, filterImageCount_thresh, filterReconstructionUncertainty_thresh, decimateMesh_size=1000000):

   # Clear the console before starting as the output lines are sent to the main function   
   PhotoScan.app.console.clear()
   

   # Construct the document class
   doc = PhotoScan.app.document




   # Add a new chunk
   chunk = doc.addChunk()

   # Crate a list to hold all the image names and fill it up  
   photoList = []
   getPhotoList(root_path, photoList)
   print ("Number of Photos found" + str(len(photoList)) )
    
   # Add the images to the project  
   chunk.addPhotos(photoList)
   
   # Check if there is a reference for the coordinates of the images, if there is a reference file add it to the project  
   isRef = False
   
   chunk.camera_location_accuracy = (0.1, 0.1, 0.1)
   
   if coordReference == "noRef":
       print("Run without reference")
       
   else:
       
       referencePath = root_path + "/" + coordReference
       
       
       chunk.loadReference(referencePath,columns ='nxzy',delimiter = " ",format = PhotoScan.ReferenceFormatNone)
   
       print("Loaded References")
       
       isRef = True

   
#   Add camera pair preselection as tuples!!!!!
   # Call the build-in function for matching photos with the specified accuracy, keypoint and tiepoint limit
   chunk.matchPhotos(accuracy=alignAccuracy, generic_preselection=True, reference_preselection=isRef, keypoint_limit=keypointLimit, tiepoint_limit=tiepointLimit)

   print("Photos matched")
   
   # Align the cameras, using adaptive fitting  
   chunk.alignCameras(adaptive_fitting = True)
   
   print("Cameras aligned")
   
   # Apply all the filters if applicable and remove the points  
   if filterReprojectionError_thresh !=0:
       f = PhotoScan.PointCloud.Filter()
       f.init(chunk, criterion = PhotoScan.PointCloud.Filter.ReprojectionError)
       f.removePoints(filterReprojectionError_thresh)
       
       print("Projection errors filtered")
   
   if filterImageCount_thresh !=0:
       f = PhotoScan.PointCloud.Filter()
       f.init(chunk, criterion = PhotoScan.PointCloud.Filter.ImageCount)
       f.removePoints(filterImageCount_thresh)
       
       print("Low image count filtered")
   
   if filterReconstructionUncertainty_thresh !=0:
       f = PhotoScan.PointCloud.Filter()
       f.init(chunk, criterion = PhotoScan.PointCloud.Filter.ReconstructionUncertainty)
       f.removePoints(filterReconstructionUncertainty_thresh)
       
       print("High reconstruction uncertainty filtered")
       
   # Align the cameras, using adaptive fitting  
   chunk.alignCameras(adaptive_fitting = True)
   # Call the buil-in function for building the depth maps, using the specified quality. The filtering of the depth map is set to moderate, so small detail is preserved     
   chunk.buildDepthMaps(quality=denseCloudQuality, filter=PhotoScan.ModerateFiltering)
   # Build the dense point cloud from the depth maps 
   chunk.buildDenseCloud()
   print("Dense point cloud created")
   # Build the mesh from the dense point cloud.   
   chunk.buildModel(surface=PhotoScan.Arbitrary, interpolation=PhotoScan.EnabledInterpolation, face_count=0)
   
   print("Mesh created")
   
   # If decimation is selected, decimate the mesh to the specified size  
   if decimateMesh_size != 0:
       
       chunk.decimateModel(face_count = decimateMesh_size)
       print("Mesh decimated")
   
   #  Get the model and the vertices     
   model = chunk.model

   verticesAll = model.vertices
    
   dir(chunk)
    
   # Save the model vertex positions and colors into a numpy array. The positions are oriented compared to to the world coordinate system of the chunk  
   allVerts = np.zeros([len(verticesAll),6])
   T = chunk.transform.matrix
   for t in range(0, len(verticesAll)) :
        
        
        point_t = T.mulp(PhotoScan.Vector([verticesAll[t].coord[0], verticesAll[t].coord[1], verticesAll[t].coord[2]]))
        
        tempVertCoord = [point_t[0], point_t[1], point_t[2],verticesAll[t].color[0], verticesAll[t].color[1], verticesAll[t].color[2]]
    
        allVerts[t] = tempVertCoord
    
   # Save the vertices as a txt file   
   np.savetxt(root_path + '/' + outputPointCloud + '.txt', allVerts, delimiter=',', fmt='%1.5f') 
   
   print("Saved vertices!")
   
   # Get the faces of the model   
   facesAll = model.faces
   
   # Save the three vertices that create the triangle for each face   
   allFaces = np.zeros([len(facesAll),3])
   
   for t in range(0, len(facesAll)) :
       
       tempFace = [facesAll[t].vertices[0], facesAll[t].vertices[1], facesAll[t].vertices[2]]
       
       allFaces[t] = tempFace

   # Save the faces as a txt file   
   faces_outputPointCloud = outputPointCloud + '_faces'
   np.savetxt(root_path + '/' + faces_outputPointCloud + '.txt', allFaces, delimiter=',', fmt='%1.5f') 
   
   print("Saved faces!")
   
   # Calculate the normal for each of the faces   
   allFaces = allFaces.astype("int32")

   onlyVerts = allVerts[:,:3]
   
   allNorms = np.zeros( onlyVerts.shape, dtype=onlyVerts.dtype )

   tris = onlyVerts[allFaces]
   
   # Calculate the normal as a cross product from the two vectors, made from the three points   
   n = np.cross( tris[::,1 ] - tris[::,0]  , tris[::,2 ] - tris[::,0] )
   
   # Normalize the normals between 0 and 1 
   normalize_v3(n)
   
   allNorms[ allFaces[:,0] ] += n
   allNorms[ allFaces[:,1] ] += n
   allNorms[ allFaces[:,2] ] += n
   normalize_v3(allNorms)
   
   # Save the normals to a text file  
   norms_outputPointCloud = outputPointCloud + '_norms'
   np.savetxt(root_path + '/' + norms_outputPointCloud + '.txt', allNorms, delimiter=',', fmt='%1.5f') 
   
   print("Saved normals!")
   
   
   
   cameraPos = []
   
   for i in range(0, len(chunk.cameras)):
       
        camera = chunk.cameras[i]

        try:
        
            position = chunk.crs.project(chunk.transform.matrix.mulp(camera.center))
        except TypeError:
            continue
    
        position = chunk.crs.project(chunk.transform.matrix.mulp(camera.center))

        cameraPos.append([position[0],position[1],position[2]])
        
   cameraPos = np.array(cameraPos)
   
   cams_outputPointCloud = outputPointCloud + '_cams'
   
   
   np.savetxt(root_path + '/' + cams_outputPointCloud + '.txt', cameraPos, delimiter=',', fmt='%1.5f')
   
   print("Saved cameras!")
    
   print("FINISED!")
   
   

   
   

#    ################################################################################################
#    ### align photos ###
#    ## Perform image matching for the chunk frame.
#    # matchPhotos(accuracy=HighAccuracy, preselection=NoPreselection, filter_mask=False, keypoint_limit=40000, tiepoint_limit=4000[, progress])
#    # - Alignment accuracy in [HighestAccuracy, HighAccuracy, MediumAccuracy, LowAccuracy, LowestAccuracy]
#    # - Image pair preselection in [ReferencePreselection, GenericPreselection, NoPreselection]
#    chunk.matchPhotos(accuracy=PhotoScan.LowAccuracy, preselection=PhotoScan.ReferencePreselection, filter_mask=False, keypoint_limit=0, tiepoint_limit=0)
#    chunk.alignCameras()
#
#    ################################################################################################
#    ### build dense cloud ###
#    ## Generate depth maps for the chunk.
#    # buildDenseCloud(quality=MediumQuality, filter=AggressiveFiltering[, cameras], keep_depth=False, reuse_depth=False[, progress])
#    # - Dense point cloud quality in [UltraQuality, HighQuality, MediumQuality, LowQuality, LowestQuality]
#    # - Depth filtering mode in [AggressiveFiltering, ModerateFiltering, MildFiltering, NoFiltering]
#    chunk.buildDenseCloud(quality=PhotoScan.LowQuality, filter=PhotoScan.AggressiveFiltering)
#
#    ################################################################################################
#    ### build mesh ###
#    ## Generate model for the chunk frame.
#    # buildModel(surface=Arbitrary, interpolation=EnabledInterpolation, face_count=MediumFaceCount[, source ][, classes][, progress])
#    # - Surface type in [Arbitrary, HeightField]
#    # - Interpolation mode in [EnabledInterpolation, DisabledInterpolation, Extrapolated]
#    # - Face count in [HighFaceCount, MediumFaceCount, LowFaceCount]
#    # - Data source in [PointCloudData, DenseCloudData, ModelData, ElevationData]
#    chunk.buildModel(surface=PhotoScan.HeightField, interpolation=PhotoScan.EnabledInterpolation, face_count=PhotoScan.HighFaceCount)
#    
#    ################################################################################################
#    ### build texture (optional) ###
#    ## Generate uv mapping for the model.
#    # buildUV(mapping=GenericMapping, count=1[, camera ][, progress])
#    # - UV mapping mode in [GenericMapping, OrthophotoMapping, AdaptiveOrthophotoMapping, SphericalMapping, CameraMapping]
#    #chunk.buildUV(mapping=PhotoScan.AdaptiveOrthophotoMapping)
#    ## Generate texture for the chunk.
#    # buildTexture(blending=MosaicBlending, color_correction=False, size=2048[, cameras][, progress])
#    # - Blending mode in [AverageBlending, MosaicBlending, MinBlending, MaxBlending, DisabledBlending]
#    #chunk.buildTexture(blending=PhotoScan.MosaicBlending, color_correction=True, size=30000)
#
#    ################################################################################################
#    ## save the project before build the DEM and Ortho images
#    doc.save()
#
#    ################################################################################################
#    ### build DEM (before build dem, you need to save the project into psx) ###
#    ## Build elevation model for the chunk.
#    # buildDem(source=DenseCloudData, interpolation=EnabledInterpolation[, projection ][, region ][, classes][, progress])
#    # - Data source in [PointCloudData, DenseCloudData, ModelData, ElevationData]
#    chunk.buildDem(source=PhotoScan.DenseCloudData, interpolation=PhotoScan.EnabledInterpolation, projection=chunk.crs)
#
#    ################################################################################################
#    ## Build orthomosaic for the chunk.
#    # buildOrthomosaic(surface=ElevationData, blending=MosaicBlending, color_correction=False[, projection ][, region ][, dx ][, dy ][, progress])
#    # - Data source in [PointCloudData, DenseCloudData, ModelData, ElevationData]
#    # - Blending mode in [AverageBlending, MosaicBlending, MinBlending, MaxBlending, DisabledBlending]
#    chunk.buildOrthomosaic(surface=PhotoScan.ModelData, blending=PhotoScan.MosaicBlending, color_correction=True, projection=chunk.crs)
#    
#    ################################################################################################
#    ## auto classify ground points (optional)
#    #chunk.dense_cloud.classifyGroundPoints()
#    #chunk.buildDem(source=PhotoScan.DenseCloudData, classes=[2])
#    
#    ################################################################################################
#    doc.save()

if __name__ == "__main__":
    # the folder needs to contain all the images and the reference file    
    
#    folder = "F:/Ivan/MilestoneMeeting_3D_reconstructions/ScanTilTest"
#    coordReference = "geotagging.txt"
#    outputPointCloud = "outputCloud_20_11_18"
#    
#    alignAccuracy = PhotoScan.MediumAccuracy
#    #add 0 if you don't want to have any limit     
#    keypointLimit = 80000
#    tiepointLimit = 80000
#    
#    denseCloudQuality = PhotoScan.MediumQuality
#    
#    #add 0 for no filter    
#    filterReprojectionError_thresh = 0.3
#    filterImageCount_thresh = 2
#    filterReconstructionUncertainty_thresh = 15
#    
#    #add 0 for no decimation
#    decimateMesh_size = 3000000

    
    
    
#    alignAccuracy = PhotoScan.MediumAccuracy
#    denseCloudQuality = PhotoScan.MediumQuality
    
    
    # This is the part that unpacks all the input parameters from the main function, to add them to the Photoscan processing function.
    # The int, float, double, etc. ones need to be changed back to the respective type from string before used.    
    folder = sys.argv[1]
    coordReference = sys.argv[2]
    outputPointCloud = sys.argv[3]
    keypointLimit = int(float(sys.argv[4]))
    tiepointLimit = int(float(sys.argv[5]))
    filterReprojectionError_thresh = float(sys.argv[6]) 
    filterImageCount_thresh =  int(float(sys.argv[7]))
    filterReconstructionUncertainty_thresh =int(float(sys.argv[8]))
    decimateMesh_size = int(float(sys.argv[9]))
    
    alignAccuracy = alignSwitcher(sys.argv[10])
    
    denseCloudQuality = densePCSwitcher(sys.argv[11])
    
#    folder = r"F:\FinalFiles\images"
#    coordReference = 'coords.txt'
#    outputPointCloud = 'scaleBlade_18_02_2019'
#    keypointLimit = int(float('80000'))
#    tiepointLimit = int(float('80000'))
#    filterReprojectionError_thresh = float('0.3') #0.3
#    filterImageCount_thresh = int(float('2')) #2
#    filterReconstructionUncertainty_thresh = int(float('15')) #15
#    decimateMesh_size = int(float('1000000'))
#    
#    alignAccuracy = alignSwitcher('A_high')
#    
#    denseCloudQuality = densePCSwitcher('PC_high')

    
    photoscanProcess(folder, coordReference, outputPointCloud, alignAccuracy, keypointLimit, tiepointLimit, denseCloudQuality, 
                     filterReprojectionError_thresh, filterImageCount_thresh, filterReconstructionUncertainty_thresh, decimateMesh_size)
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 10 15:20:06 2018

@author: ivan
"""
import numpy as np
import PhotoScan



doc = PhotoScan.app.document
chunk = doc.chunk
point_cloud = chunk.point_cloud
point_proj = point_cloud.projections


cameraAngles = []
cameraPos = []
cameraNames = []

cameraNums = []


cameraNormals = []

cameraPerp = []


pointArray = []

points = point_cloud.points
npoints = len(points)
T = chunk.transform.matrix



#for k in range(0, len(chunk.cameras)):
#    
#    photo = chunk.cameras[k]
#    	
#    point_index = 0
#    pointsCurr = []
#    for proj in point_proj[photo]:
#        
#        track_id = proj.track_id
#        while point_index < npoints and points[point_index].track_id < track_id:
#            point_index += 1
#        if point_index < npoints and points[point_index].track_id == track_id:
#            if not points[point_index].valid: 
#                continue	
#            else:
#                point_t = T.mulp(PhotoScan.Vector([points[point_index].coord[0], points[point_index].coord[1], points[point_index].coord[2]]))
#                pointsCurr.append([k, point_t[0], point_t[1], point_t[2]])
#                points[point_index].selected = True
#    
#    pointArray += pointsCurr
#
#pointArray= np.array(pointArray)



for i in range(0, len(chunk.cameras)):
    camera = chunk.cameras[i]

    try:
        
        position = chunk.crs.project(chunk.transform.matrix.mulp(camera.center))
    except TypeError:
        continue
    
    position = chunk.crs.project(chunk.transform.matrix.mulp(camera.center))
    


    v_int = camera.transform.mulv(PhotoScan.Vector([0,0,1]))
    cameraNormal = chunk.transform.matrix.mulv(v_int)
    
    v_int2 = camera.transform.mulv(PhotoScan.Vector([0,-1,0]))
    cameraTang = chunk.transform.matrix.mulv(v_int2)
    
    
    
    
    print("Camera Normal - " + str(cameraNormal) )
    print("Camera Position - " + str(position) )
    
    cameraPos.append([position[0],position[1],position[2]])
    
    cameraNormals.append([cameraNormal[0],cameraNormal[1],cameraNormal[2]])
    
    cameraPerp.append([cameraTang[0],cameraTang[1],cameraTang[2]])
    
    

    	
    point_index = 0
    pointsCurr = []
    for proj in point_proj[camera]:
        
        track_id = proj.track_id
        while point_index < npoints and points[point_index].track_id < track_id:
            point_index += 1
        if point_index < npoints and points[point_index].track_id == track_id:
            if not points[point_index].valid: 
                continue	
            else:
                point_t = T.mulp(PhotoScan.Vector([points[point_index].coord[0], points[point_index].coord[1], points[point_index].coord[2]]))
                pointsCurr.append([i, point_t[0], point_t[1], point_t[2]])
                points[point_index].selected = True
    
    pointArray += pointsCurr



cameraPos = np.array(cameraPos)
cameraNormals = np.array(cameraNormals)
cameraPerp = np.array(cameraPerp)

pointArray= np.array(pointArray)


np.savetxt(r"F:\Ivan\ScalePaper_photos\Blade_photos\cameraPos.txt",cameraPos, delimiter=',')

np.savetxt(r"F:\Ivan\ScalePaper_photos\Blade_photos\cameraNorm.txt",cameraNormals, delimiter=',')

np.savetxt(r"F:\Ivan\ScalePaper_photos\Blade_photos\cameraPerp.txt",cameraPerp, delimiter=',')

np.savetxt(r"F:\Ivan\ScalePaper_photos\Blade_photos\sparsePC.txt",pointArray, delimiter=',')


print("Region Position")
print(T.mulp(PhotoScan.Vector([chunk.region.center[0], chunk.region.center[1], chunk.region.center[2]])))


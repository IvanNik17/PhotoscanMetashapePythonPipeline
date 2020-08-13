# -*- coding: utf-8 -*-
"""
Created on Thu Dec 20 09:11:33 2018

@author: ivan
"""

import numpy as np


def makeObjFile(filename, verts, faces, normals):
    
    faces = faces.astype(int)
    
    faces=faces +1

    thefile = open(filename, 'w')
    for item in verts:
      thefile.write("v {0} {1} {2}\n".format(item[0],item[1],item[2]))
    
    for item in normals:
      thefile.write("vn {0} {1} {2}\n".format(item[0],item[1],item[2]))
    
    for item in faces:
      thefile.write("f {0}//{0} {1}//{1} {2}//{2}\n".format(item[0],item[1],item[2]))  
    
    thefile.close()


#if 'bladeVerts' not in  locals():
#    bladeVerts = np.loadtxt("blade_500k_verts.txt")
#    
#    
#if 'bladeFaces' not in  locals():
#    bladeFaces = np.loadtxt("blade_500k_faces.txt")


if __name__ == "__main__":

    if 'bladeVerts' not in  locals():
        bladeVerts = np.loadtxt(r"F:\Ivan\ScalePaper_photos\Scale_ArtefactForCalibration2\scaleBlade_18_02_2019.txt", delimiter = ',')
        
        
    if 'bladeFaces' not in  locals():
        bladeFaces_float = np.loadtxt(r"F:\Ivan\ScalePaper_photos\Scale_ArtefactForCalibration2\scaleBlade_18_02_2019_faces.txt", delimiter = ',')
    
    if 'bladeNormals' not in  locals():
        bladeNormals = np.loadtxt(r"F:\Ivan\ScalePaper_photos\Scale_ArtefactForCalibration2\scaleBlade_18_02_2019_norms.txt", delimiter = ',')
    
    
    bladeColors = bladeVerts[:,3:]
    bladeFaces = bladeFaces_float.astype(int)
    
    bladeVerts= bladeVerts[:,:3]*1000
    
    bladeFaces=bladeFaces +1
    
    thefile = open(r"F:\Ivan\ScalePaper_photos\Blade_photos\scaleBlade.obj", 'w')
    for item in bladeVerts:
      thefile.write("v {0} {1} {2}\n".format(item[0],item[1],item[2]))
    
    for item in bladeNormals:
      thefile.write("vn {0} {1} {2}\n".format(item[0],item[1],item[2]))
    
    for item in bladeFaces:
      thefile.write("f {0}//{0} {1}//{1} {2}//{2}\n".format(item[0],item[1],item[2]))  
    
    thefile.close()


#blade_verts = bladeVerts[:,:3]*1000
#blade_norms = bladeVerts[:,3:6]
#blade_colors = bladeVerts[:,6:]
#
#blade_faces = bladeFaces[:,1:]
#blade_faces = blade_faces.astype(int)
#
#blade_faces=blade_faces +1
#
#thefile = open('test.obj', 'w')
#for item in blade_verts:
#  thefile.write("v {0} {1} {2}\n".format(item[0],item[1],item[2]))
#
#for item in blade_norms:
#  thefile.write("vn {0} {1} {2}\n".format(item[0],item[1],item[2]))
#
#for item in blade_faces:
#  thefile.write("f {0}//{0} {1}//{1} {2}//{2}\n".format(item[0],item[1],item[2]))  
#
#thefile.close()
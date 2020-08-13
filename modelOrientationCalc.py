# -*- coding: utf-8 -*-
"""
Created on Thu Sep 27 08:38:34 2018

@author: ivan
"""

import numpy as np
#from sklearn.decomposition import PCA
#from scipy import stats
import math


import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def set_axes_equal(ax):


    x_limits = ax.get_xlim3d()
    y_limits = ax.get_ylim3d()
    z_limits = ax.get_zlim3d()

    x_range = abs(x_limits[1] - x_limits[0])
    x_middle = np.mean(x_limits)
    y_range = abs(y_limits[1] - y_limits[0])
    y_middle = np.mean(y_limits)
    z_range = abs(z_limits[1] - z_limits[0])
    z_middle = np.mean(z_limits)

    # The plot bounding box is a sphere in the sense of the infinity
    # norm, hence I call half the max range the plot radius.
    plot_radius = 0.5*max([x_range, y_range, z_range])

    ax.set_xlim3d([x_middle - plot_radius, x_middle + plot_radius])
    ax.set_ylim3d([y_middle - plot_radius, y_middle + plot_radius])
    ax.set_zlim3d([z_middle - plot_radius, z_middle + plot_radius])


    
pc_file = r"F:\\FinalFiles\\images\\" + "testBlade.txt"

if 'pointCloud' not in  locals():
    pointCloud = np.loadtxt(pc_file, delimiter = ",")
#
#    
pointCloud_small = pointCloud[::300,:]
#    
pointCloud_points = pointCloud_small[:,:3]
#
pointCloud_color = pointCloud_small[:,3:]



meanX = pointCloud_points[:,0].mean()
meanY = pointCloud_points[:,1].mean()
meanZ = pointCloud_points[:,2].mean()

pointCloud_points[:,0] -= meanX
pointCloud_points[:,1] -= meanY
pointCloud_points[:,2] -= meanZ


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.scatter(pointCloud_points[:,0], pointCloud_points[:,1], pointCloud_points[:,2], facecolors=pointCloud_color/255, marker=".", edgecolors='none')


pointCloud_points_xy = pointCloud_points[:,0:2]
pointCloud_points_xz = pointCloud_points[:,[0,2]]
pointCloud_points_yz = pointCloud_points[:,[1,2]]

#pointCloud_points_xz[:,0] = -1* pointCloud_points_xz[:,0] 



#----------------------------
fig1 = plt.figure()
#ax1 = fig1.add_subplot(131)
#ax1.scatter(pointCloud_points_xy[:,0], pointCloud_points_xy[:,1])
#ax1.axis("equal")



ax2 = fig1.add_subplot(111)
ax2.scatter(pointCloud_points_xz[:,0], pointCloud_points_xz[:,1])




#ax3 = fig1.add_subplot(133)
#ax3.scatter(pointCloud_points_yz[:,0], pointCloud_points_yz[:,1])
#ax3.axis("equal")

# -------------------------------
#pca_xy = PCA(n_components=1)
#pca_xy.fit(pointCloud_points_xy)
#pcaTrans_xy = pca_xy.transform(pointCloud_points_xy)
#rep_xy = pca_xy.inverse_transform(pcaTrans_xy)
#ax1.scatter(rep_xy[:,0], rep_xy[:,1], c= 'r')
#
#pca_xz = PCA(n_components=1)
#pca_xz.fit(pointCloud_points_xz)
#pcaTrans_xz = pca_xz.transform(pointCloud_points_xz)
#rep_xz = pca_xz.inverse_transform(pcaTrans_xz)
#ax2.scatter(rep_xz[:,0], rep_xz[:,1] , c= 'r')
#
#
#pca_yz = PCA(n_components=1)
#pca_yz.fit(pointCloud_points_yz)
#pcaTrans_yz = pca_yz.transform(pointCloud_points_yz)
#rep_yz = pca_yz.inverse_transform(pcaTrans_yz)
#ax3.scatter(rep_yz[:,0], rep_yz[:,1], c= 'r')

#------------------------

cov_mat = np.cov(pointCloud_points_xz.T)
eig_val_cov, eig_vec_cov = np.linalg.eig(cov_mat)
maxIndEigenval = np.argmax(eig_val_cov)
evec1 = eig_vec_cov[:,maxIndEigenval]

angleOffsetMeasured = math.degrees(np.arctan2( evec1[0],evec1[1]   )) 
#if angleOffsetMeasured < 0:
#    angleOffsetMeasured =  angleOffsetMeasured + 180
    
print(angleOffsetMeasured)
    
#angleOffsetMeasured = 180 - angleOffsetMeasured

angleOffsetMeasured3d = -angleOffsetMeasured

angleOffsetMeasured*=math.pi/180
    
pointCloud_points_xz_rot = pointCloud_points_xz.copy()

pointCloud_points_rot = pointCloud_points.copy()

    
ax2.axis("equal")

pointCloud_points_xz_rot[:,0] = pointCloud_points_xz[:,0] * np.cos(angleOffsetMeasured) - pointCloud_points_xz[:,1] * np.sin(angleOffsetMeasured)
pointCloud_points_xz_rot[:,1] = pointCloud_points_xz[:,0] * np.sin(angleOffsetMeasured) + pointCloud_points_xz[:,1] * np.cos(angleOffsetMeasured)

ax2.scatter(pointCloud_points_xz_rot[:,0], pointCloud_points_xz_rot[:,1], c = "r")


angleOffsetMeasured3d*=math.pi/180

#pointCloud_points_rot[:,0] = pointCloud_points[:,0] * np.cos(angleOffsetMeasured3d) - pointCloud_points[:,2] * np.sin(angleOffsetMeasured3d)
#pointCloud_points_rot[:,2] = pointCloud_points[:,2] * np.sin(angleOffsetMeasured3d) + pointCloud_points[:,2] * np.cos(angleOffsetMeasured3d)

pointCloud_points_rot[:,0] = pointCloud_points[:,0] * np.cos(angleOffsetMeasured3d) + pointCloud_points[:,2] * np.sin(angleOffsetMeasured3d)

pointCloud_points_rot[:,2] = pointCloud_points[:,2] * np.cos(angleOffsetMeasured3d) - pointCloud_points[:,0] * np.sin(angleOffsetMeasured3d)


ax.scatter(pointCloud_points_rot[:,0], pointCloud_points_rot[:,1], pointCloud_points_rot[:,2],c='r', marker=".", edgecolors='none')


set_axes_equal(ax)


# -*- coding: utf-8 -*-
"""
Created on Mon Oct  8 14:56:54 2018

@author: ivan
"""

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

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

def initializePlot3D(mainBlade_points, mainBlade_colors):
#    fig3d_anim = plt.figure()
#    
#    ax = fig3d_anim.add_subplot(1,1,1)
#    
#    ax = Axes3D(fig3d_anim)
    
    
    fig, ax = plt.subplots(1,1, subplot_kw={'projection':'3d', 'aspect':'equal'})

    ax.view_init(elev=10., azim=40)

    
    graphMain = ax.scatter(mainBlade_points[:,0], mainBlade_points[:,1], mainBlade_points[:,2], facecolors=mainBlade_colors/255, marker=".", edgecolors='none')
    graphBand, = ax.plot([0], [0], [0], 'ro')
    

    
    
    ax.set_xlabel("X Axis")
    ax.set_ylabel("Y Axis")
    ax.set_zlabel("Z Axis")
    
    
    
#    ax.axis([-axisSize, axisSize, -axisSize, axisSize])

#    ax.set_xlim(-axisSize, axisSize)
#    ax.set_ylim(-axisSize, axisSize)
#    ax.set_zlim(-axisSize, axisSize)
    
    title = ax.set_title('Blade segment')
    
    
    return ax, title, graphBand, 
    
    
def plot3D_animate(ax,title, graphBand, currPoints, currHeight, maxHeight):
    
    graphBand.set_data (currPoints[:,0], currPoints[:,1])
    
    graphBand.set_3d_properties(currPoints[:,2])
    
    set_axes_equal(ax)
   
    title.set_text('Blade segment at height ' + str("{:.3f}".format(currHeight)) + ' from max ' +str( "{:.3f}".format(maxHeight)))
    
    plt.pause(0.0001)  
    
def closeFigures():
    plt.close()
    

#if __name__ == '__main__': 
#    
#    import numpy as np
#    
#    title, graphDrone, graphEnv, = initializePlot(1000)
#    
#    dronePos =np.array( [345, 566]) 
#    bladePointsPos = np.array( [[456, 334]])
#
#    height = 200
#    
#    lidarRotAngle = 30
#    
#    try:
#        
#        while True:
#            plot3D_animate(title, graphDrone, graphEnv ,dronePos, bladePointsPos, height, lidarRotAngle)
#            height +=1
#            
#    except KeyboardInterrupt:
#        print("end")
    
    
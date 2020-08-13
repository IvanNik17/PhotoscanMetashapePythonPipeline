# -*- coding: utf-8 -*-
"""
Created on Mon Oct  8 14:57:57 2018

@author: ivan
"""

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

    

def initializePlot():
    fig2d_anim = plt.figure()
    
    ax = fig2d_anim.add_subplot(1,1,1)
    
    slice2D, = ax.plot([0], [0], 'ro')

    
    
    ax.set_xlabel("X Axis")
    ax.set_ylabel("Y Axis")
    
#    ax.axis([-1, 1, -1, 1])
    title = ax.set_title('Current slice')
    
    
    return ax, title, slice2D,
    
    
def plot2D_animate(ax, title, slice2D, sliceData, currHeight, maxHeight, visulAxis):
    
    slice2D.set_data (sliceData[:,visulAxis[0]], sliceData[:,visulAxis[1]])
    
    
    title.set_text('Current slice at height ' + str(currHeight) + " from " + "{:.3f}".format(maxHeight))
    

    
#        find the maximum range of the x,y and z data
    max_range = [max(sliceData[:,2]),max(sliceData[:,2])]
#       find the mid points of the ranges
    mid_x = (max(sliceData[:,0])+min(sliceData[:,0])) * 0.5
    mid_y = (max(sliceData[:,2])+min(sliceData[:,2])) * 0.5

#       set the limits of the axes of the figure so the always contain the full data
    ax.set_xlim(mid_x - max_range[0], mid_x + max_range[0])
    ax.set_ylim(mid_y - max_range[1], mid_y + max_range[1])


    
    plt.pause(0.001)  
    
def closeFigures():
    plt.close()
    



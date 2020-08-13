# -*- coding: utf-8 -*-
"""
Created on Fri Jun  1 12:43:04 2018

@author: ivan
"""

import numpy
import math


    
"""
## References
- [Umeyama's paper](Least-squares estimation of transformation parameters between two point patterns)
- [CarloNicolini's python implementation](https://gist.github.com/CarloNicolini/7118015)
"""    
    
def similarity_transform(from_points, to_points):
    
    assert len(from_points.shape) == 2, \
        "from_points must be a m x n array"
    assert from_points.shape == to_points.shape, \
        "from_points and to_points must have the same shape"
    
    N, m = from_points.shape
    
    mean_from = from_points.mean(axis = 0)
    mean_to = to_points.mean(axis = 0)
    
    delta_from = from_points - mean_from # N x m
    delta_to = to_points - mean_to       # N x m
    
    sigma_from = (delta_from * delta_from).sum(axis = 1).mean()
    sigma_to = (delta_to * delta_to).sum(axis = 1).mean()
    
    cov_matrix = delta_to.T.dot(delta_from) / N
    
    U, d, V_t = numpy.linalg.svd(cov_matrix, full_matrices = True)
    cov_rank = numpy.linalg.matrix_rank(cov_matrix)
    S = numpy.eye(m)
    
    if cov_rank >= m - 1 and numpy.linalg.det(cov_matrix) < 0:
        S[m-1, m-1] = -1
    elif cov_rank < m-1:
        raise ValueError("colinearility detected in covariance matrix:\n{}".format(cov_matrix))
    
    R = U.dot(S).dot(V_t)
    c = (d * S.diagonal()).sum() / sigma_from
    t = mean_to - c*R.dot(mean_from)
    
    return c*R,c,R, t


def scaleAndUncertanty(groundPoints, recPoints, stdDev):
    
    M_init,c_init,R, t_init = similarity_transform(recPoints,  groundPoints)
    stdDevXY = stdDev[0]
    stdDevZ = stdDev[1]

    
    allScales_newMethod_plus = numpy.zeros([len(groundPoints),3])
    allScales_newMethod_minus = numpy.zeros([len(groundPoints),3])



    for k in range(0,len(groundPoints)):
        for n in range(0,3):
            for l in range(0,2):
                
                groundPoints_test = []
                groundPoints_test = groundPoints.copy()
                
                if n == 0 or n == 1:
                    dimDev = stdDevXY
                else:
                    dimDev = stdDevZ
                
                if l == 0:
                    dimDev = dimDev
                else:
                    dimDev = -dimDev
                
                groundPoints_test[k,n] += dimDev

                M,c_new,R, t = similarity_transform(recPoints,  groundPoints_test)
                
                if l == 0:

                    allScales_newMethod_plus[k,n] = c_new
                else:
                    allScales_newMethod_minus[k,n] = c_new
                    
            

    allScales_newMethod_finalX = (allScales_newMethod_plus[:,0] - allScales_newMethod_minus[:,0])/(2*stdDevXY)
    allScales_newMethod_finalY = (allScales_newMethod_plus[:,1] - allScales_newMethod_minus[:,1])/(2*stdDevXY)
    allScales_newMethod_finalZ = (allScales_newMethod_plus[:,2] - allScales_newMethod_minus[:,2])/(2*stdDevZ)
    
    
    
    finalAll = numpy.zeros([1,3*len(allScales_newMethod_finalX)])
    
    for q in range(0,len(finalAll[0]),3):
        finalAll[0,q] = allScales_newMethod_finalX[int(q/3)]
        finalAll[0,q+1] = allScales_newMethod_finalY[int(q/3)]
        finalAll[0,q+2] = allScales_newMethod_finalZ[int(q/3)]
    
    firstSecondLine = numpy.ones((1,len(groundPoints)*3))*stdDevXY**2
    thirdLine = numpy.ones((1,len(groundPoints)*3))*stdDevZ**2
    combinedThree = numpy.concatenate([firstSecondLine,firstSecondLine,thirdLine])
    fullCombined = combinedThree.copy()
    for j in range(0,len(groundPoints)-1):
        fullCombined = numpy.concatenate([fullCombined,combinedThree])
    
    fullCombined[~numpy.eye(fullCombined.shape[0],dtype=bool) == True] = 0
    
    
    
    #scaleTest = numpy.linalg.multi_dot([finalAll, fullCombined,finalAll.T])
    scaleTest_temp = numpy.dot(fullCombined, numpy.transpose(finalAll))
    uncentainty = numpy.dot(finalAll, scaleTest_temp)
    
    
    return [c_init, math.sqrt(uncentainty)]
    
        
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 18 11:51:31 2018

@author: aviasayag
"""

import numpy as np





def print1(isPrint ,strToPrint):
    if(isPrint):
        print(strToPrint)
        
        
        

"""
Returns a matrix of size n*n where in the (i,j) place is the number of the 
different txs in the block i built vs the block j built.
"""
def compareBlocks(blocksList, isPrint=1):
    numOfBlocks = len(blocksList)
    missingMat = range(numOfBlocks**2)
    missingMat = np.reshape(missingMat, (numOfBlocks, numOfBlocks))
    
    for i in range(numOfBlocks):
        block1 = blocksList[i]
        size1 = len(block1)
        
        for j in range(i, numOfBlocks):
            block2 = blocksList[j]
            size2 = len(block2)
            
            togetherSize = len(set(block1+block2))
            missingNum1 = togetherSize - size1
            missingNum2 = togetherSize - size2
            
            missingMat[i][j] = missingNum1
            missingMat[j][i] = missingNum2
            
    print1(isPrint, missingMat)
    return missingMat


"""
Returns a matrix of size n*n where in the (i,j) place is the number of the 
different txs in the i's epool vs j's epool.
"""
def compareEpools(nodesList, isPrint=1):
    numOfNodes = len(nodesList)
    missingMat = range(numOfNodes**2)
    missingMat = np.reshape(missingMat, (numOfNodes, numOfNodes))
    
    for i in range(numOfNodes):
        epool1 = nodesList[i].epool
        size1 = len(epool1)
        
        for j in range(i, numOfNodes):
            epool2 = nodesList[j].epool
            size2 = len(epool2)
            
            togetherSize = len(set(epool1+epool2))
            missingNum1 = togetherSize - size1
            missingNum2 = togetherSize - size2
            
            missingMat[i][j] = missingNum1
            missingMat[j][i] = missingNum2
            
    print1(isPrint, missingMat)
    return missingMat



"""
"""
def meanMatrixWithoutDiagonal(mat):
    
    length, width = mat.shape
    count = 0
    summ = 0
    
    for i in range(length):
        for j in range(width):
            if i != j:
                count += 1
                summ += mat[i][j]
    
    return summ/count
        
        
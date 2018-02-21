#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 18 15:27:36 2018

@author: aviasayag
"""

import node
import epool
import block
import utils
import numpy as np
import time
 



def print1(isPrint ,strToPrint):
    if(isPrint):
        print(strToPrint)




class Simulator:
    
    """
    Initial setup of the simulation.
    1) create nodes each with the same epoolSample
    2) create global epool by epoolSize
    3) each node chooses its txs from the global epool (by its sample)
    """
    def __init__(self, nodesNum, epoolSample, epoolSize, isPrint=1):
        
        start = time.process_time()
        
        self.isPrint = isPrint
        self.nodesNum = nodesNum
        self.nodesList = node.createNodes(nodesNum, epoolSample)
        
        end = time.process_time()
        print1(isPrint, "Time elapsed (createNodes): %s" % (end-start))
        
        self.globalEpool = epool.createGlobalEpool(self.nodesList, epoolSize)
        end = time.process_time()
        print1(isPrint, "Time elapsed (createGlobalEpool): %s" % (end-start))
        
        epool.chooseTXs(self.nodesList, self.globalEpool)
        end = time.process_time()
        print1(isPrint, "Time elapsed (chooseTXs): %s" % (end-start))
                
        # print initial setup statisitics
        print1(isPrint, "Total nodes: %s  || Global epool size: %s" \
              % (len(self.nodesList), len(self.globalEpool)))

        print1(isPrint, "-----------------")
        
        for nd in self.nodesList:
            print1(isPrint, "Node %s: (epool size: %s), (epool sample: %s), (global epool portion: %s)" % \
                  (nd.index, nd.epoolSize, nd.sample, nd.portion))
        
        print1(isPrint, "-----------------")
        
        epoolCompareMat = utils.compareEpools(self.nodesList, isPrint)
        avg = utils.meanMatrixWithoutDiagonal(epoolCompareMat)
        np.fill_diagonal(epoolCompareMat, avg) # so min won't return 0
        
        print1(isPrint, "avg epool diff: %s || max diff: %s || min diff: %s" % \
              (avg, epoolCompareMat.max(), epoolCompareMat.min()))
    
        print1(isPrint, "-----------------")
        
        end = time.process_time()
        print1(isPrint, "Time elapsed (initial setup): %s" % (end-start))
    
        print1(isPrint, "-----------------")
        print1(isPrint, "-----------------")
        
    
    """
    Simulate the b txs with minimum hash 
    """
    def sim1(self, numTxInBlock):
        
        print1(self.isPrint, "")
        print1(self.isPrint, "==== Simulation 1 =====")
        return genericSim(self.nodesList, self.isPrint, 0,
                   block.buildGoodEblock, numTxInBlock)
        
        

    """
    Simulate the b txs with constant threshold 
    """
    def sim2(self, numTxInBlock, threshold):
        
        print1(self.isPrint, "")
        print1(self.isPrint, "==== Simulation 2A =====")
        return genericSim(self.nodesList, self.isPrint, 0,
                   block.buildGoodEblockConstThreshold, numTxInBlock, threshold)


    """
    Simulate the b txs with constant threshold .
    Here, we check how many txs we could have insert
    """
    def sim2B(self, threshold):
        
        print1(self.isPrint, "")
        print1(self.isPrint, "==== Simulation 2B =====")
        return genericSim(self.nodesList, self.isPrint, 1,
                   epool.sliceEpoolByThreshold, threshold)
        

    

"""
Generic simulation
"""
def genericSim(nodesList, isPrint, isCount, func, *args):
    start = time.process_time()

    blocks = []
    
    totalTxs = 0
    # build block for each node
    for nd in nodesList:
        blockToAppend = func(nd, *args)
        blocks.append(blockToAppend)
        if isCount:
            blockSize = len(blockToAppend)
            totalTxs += blockSize
            print1(isPrint, "Node %s txs under threshold: %s" % (nd.index, blockSize))
            
    if isCount:
        print1(isPrint, "under threshold (avg: %s)" % (totalTxs/len(blocks)))
    
    blockCompMat = utils.compareBlocks(blocks, isPrint)
    avg = utils.meanMatrixWithoutDiagonal(blockCompMat)
    
    np.fill_diagonal(blockCompMat, avg) # so min won't return 0
    
    mini = blockCompMat.min()
    maxi = blockCompMat.max()
    
    print1(isPrint, "avg block diff: %s || max diff: %s || min diff: %s" % \
          (avg, maxi, mini))
    
    print1(isPrint, "-----------------")
    
    end = time.process_time()
    print1(isPrint, "Time elapsed (sim): %s" % (end-start))
    
    return (avg, mini, maxi)







 






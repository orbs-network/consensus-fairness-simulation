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
import math
 



def print1(isPrint ,strToPrint):
    if(isPrint):
        print(strToPrint)




class EblockSimulator:
    
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




 
class FairnessSimulator:
    
    """
    Initial setup of the fairness simulation.

    1) create nodes each with the same epoolSample.
    2) the first node is byzantine, make its epool sample to be 100%, i.e., the byzantine knows all the
    transactions.
    3) create global epool by epoolSize. The byzantine node has more etx in the global epool by factor
    of (byznatineNum/nodesNum)
    4) each node chooses its txs from the global epool (by its sample)
    """
    def __init__(self, nodesNum, byzantineNum, epoolSample, epoolSize, isPrint=1):
        
        start = time.process_time()
        
        self.globalEpoolSize = epoolSize
        self.isPrint = isPrint
        self.nodesNum = nodesNum
        self.byzantineNum = byzantineNum
        self.nodesList = node.createNodesWithSingleByzantine(nodesNum, byzantineNum, epoolSample)

        end = time.process_time()
        print1(isPrint, "Time elapsed (createNodes): %s" % (end-start))
        
        self.globalEpool = epool.createGlobalEpool(self.nodesList, epoolSize)
        end = time.process_time()
        print1(isPrint, "Time elapsed (createGlobalEpool): %s" % (end-start))
        
        epool.chooseTXs(self.nodesList, self.globalEpool)
        end = time.process_time()
        print1(isPrint, "Time elapsed (chooseTXs): %s" % (end-start))
                
        # print initial setup statisitics
        if(isPrint):
            self.printInitialSetup(start)
        

    def printInitialSetup(self, start):
        isPrint = self.isPrint

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
    All nodes construct valid Eblocks
    """
    def allConstructValidEblocks(self, numTxInBlock):
        
        print1(self.isPrint, "")
        print1(self.isPrint, "==== Valid Eblock Construction =====")

        start = time.process_time()
        blocks = []

        # build block for each node
        for nd in self.nodesList:
            blockToAppend = block.buildGoodEblock(nd, numTxInBlock)
            nd.block = blockToAppend
            blocks.append(blockToAppend)
                
        blockCompList = utils.compareBlocksWithByzantine(blocks, self.isPrint)
        avg = np.average(blockCompList[1:])
                
        mini = np.min(blockCompList[1:])
        maxi = np.max(blockCompList[1:])
        
        print1(self.isPrint, "avg block diff: %s || max diff: %s || min diff: %s" % \
            (avg, maxi, mini))
        
        print1(self.isPrint, "-----------------")
        
        end = time.process_time()
        print1(self.isPrint, "Time elapsed (sim): %s" % (end-start))
        
        return (avg, mini, maxi)


    """
    After a Byzantine nodes constructed a valid Eblock it manipulates a 
    (1-beta)-fraction of its Eblock by removing all the etxs (that he is not the owner) 
    that have maximal hash value in its block and replacing it with it own.
    """
    def byzantineManipulateItsBlock(self, beta):
        byzantine = self.nodesList[0]
        block = byzantine.block
        blockSize = len(block)

        # update epool without the blocks selected transactions
        byzantineEpool = set(byzantine.epool).difference(block)
        byzantineEpool = [i for i in byzantineEpool if i.source == 0]

        sortedEpool = sorted(byzantineEpool, \
                              key=lambda tx: tx.sha256ToInt("%s" % (tx.source)))
        
        epoolSize = len(sortedEpool)
        numOfTxsToReplace = math.ceil(blockSize * (1 - beta))
        print1(self.isPrint, "replace %s txs" % (numOfTxsToReplace))

        countReplaced = 0
        blockIndex = blockSize-1
        epoolIndex = 0
        
        while (countReplaced < numOfTxsToReplace and blockIndex > -1 
            and epoolIndex < epoolSize):

            # Replace only non-Byzantine txs
            if block[blockIndex].source != 0:
                block[blockIndex] = sortedEpool[epoolIndex]
                epoolIndex += 1
                countReplaced += 1

            blockIndex -= 1


        print1(self.isPrint, "%s txs replaced" % (countReplaced))
        return block
        

    """
    Each node validates the proposed Byzantine's Eblock by the beta parameter
    (i.e., each of the nodes looks for at least beta-fraction intersection 
    between its Eblock to the Byzantine's Eblock). 

    Returns the number of nodes that negative validated the Eblock.
    """
    def validateEblocks(self, beta):

        txsDiffThreshold = math.ceil(len(self.nodesList[0].block) * (1 - beta))
        print1(self.isPrint, "Validation threshold %s:" %(txsDiffThreshold))
        blocks = []

        # build block for each node
        for nd in self.nodesList:
            blocks.append(nd.block)

        blockCompList = utils.compareBlocksWithByzantine(blocks, self.isPrint)
        avg = np.average(blockCompList[1:])
                
        mini = np.min(blockCompList[1:])
        maxi = np.max(blockCompList[1:])
        
        print1(self.isPrint, "avg block diff: %s || max diff: %s || min diff: %s" % \
            (avg, maxi, mini))

        notPassedValidation = list(map(lambda diff: 0 if diff <= txsDiffThreshold else 1, blockCompList))
        
        print1(self.isPrint, notPassedValidation)

        numOfNotPassed = sum(notPassedValidation)
        print1(self.isPrint, "Number nodes that did not passed the block is %s " % (numOfNotPassed))
        print1(self.isPrint, "-----------------")
                
        return numOfNotPassed

    
    """
    This function takes a block and extract it from each node's Epool
    as well as the global Epool. Later, the global Epool and the nodes'
    epools are being filled with new txs by each node's initial portion.
    """
    def inputNewTxs(self, blockToExtract):
        start = time.process_time()

        # update all Epools without the extracted block
        self.globalEpool = list(set(self.globalEpool).difference(blockToExtract))
        for nd in self.nodesList:
            nd.epool = list(set(nd.epool).difference(blockToExtract))
        
        # Fill global Epool by each node portion
        addToGlobalEpool = epool.createGlobalEpool(self.nodesList, len(blockToExtract))
        self.globalEpool += addToGlobalEpool

        # Add the new txs to each node epool by it sampling
        epool.chooseTXs(self.nodesList, addToGlobalEpool)

        if self.isPrint:
            self.printInitialSetup(start)

    
    """
    Returns nodes' distribution in the global Epool
    """
    def getGlobalEpoolDist(self):
        return epool.getNodesDistribution(self.globalEpool, self.nodesNum)
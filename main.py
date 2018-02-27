#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 18 15:10:11 2018

@author: aviasayag
"""

import utils
import simulator
import time



# Parameters
NODES_NUM = 10
BYZANTINE_NUM = 2
EPOOL_SIZE = 10000

EPOOL_SAMPLE = 0.9 # num between 0 to 1
NUM_TX_IN_BLOCK = 1000


"""
An example for an Eblock construction simulation
"""
def simulateEblockConstructionMethods(nodesNum, epoolSample, epoolSize, txsInBlock):

    sim = simulator.EblockSimulator(nodesNum, epoolSample, epoolSize, 1)
    
    sim.sim1(txsInBlock)
    
    threshold = (txsInBlock/9000) * (2**256)
    sim.sim2(txsInBlock, threshold)
    
    sim.sim2B(threshold)

"""
Simulate the manipulation byzantine node can do when constructing an
"""
def simulateByzantineFairnessManipulation(nodesNum, byzantineNum, epoolSample, epoolSize, txsInBlock):
    
    sim = simulator.FairnessSimulator(nodesNum, byzantineNum, epoolSample, epoolSize, 1)

    sim.allConstructValidEblocks(txsInBlock)

if __name__ == '__main__':
        
    #simulateEblockConstructionMethods(NODES_NUM, EPOOL_SAMPLE, EPOOL_SIZE, NUM_TX_IN_BLOCK)
    simulateByzantineFairnessManipulation(NODES_NUM, BYZANTINE_NUM, EPOOL_SAMPLE, \
        EPOOL_SIZE, NUM_TX_IN_BLOCK)
    
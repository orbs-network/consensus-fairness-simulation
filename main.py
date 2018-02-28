#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 18 15:10:11 2018

@author: aviasayag
"""

import utils
import simulator
import time
import numpy as np


# Parameters
NODES_NUM = 10
BYZANTINE_NUM = 2
EPOOL_SIZE = 10000

EPOOL_SAMPLE = 0.95 # num between 0 to 1
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
def simulateByzantineFairnessManipulation(nodesNum, byzantineNum, epoolSample, epoolSize, 
    txsInBlock, beta, manipulationBeta):
    
    sim = simulator.FairnessSimulator(nodesNum, byzantineNum, epoolSample, epoolSize, 1)

    sim.allConstructValidEblocks(txsInBlock)

    sim.byzantineManipulateItsBlock(manipulationBeta)
    return sim.validateEblocks(beta)


"""
Analysis for the question: "How much of the Eblock can Byzantine
node manipulate so it would still be valid in the other nodes eyes?"
"""
def manipulationAnalysis():
    beta = EPOOL_SAMPLE ** 2 - ((10/NUM_TX_IN_BLOCK) ** (0.5))

    avgTries = 20
    betaTries = 10
    factor = 1.044
    betaManipulation = beta * factor
    
    for j in range (betaTries):

        avgList = []
        for i in range(avgTries):
            fails = simulateByzantineFairnessManipulation(NODES_NUM, BYZANTINE_NUM,  \
                EPOOL_SAMPLE, EPOOL_SIZE, NUM_TX_IN_BLOCK, beta, betaManipulation)
            avgList.append(fails / (NODES_NUM-1))

        avg = sum(avgList)/avgTries
        minAvg = min(avgList)
        maxAvg = max(avgList)
        stdDeviation = (sum(map(lambda x: (x-avg)**2, avgList)) / (avgTries-1)) ** 0.5

        print(
"""beta: %s, beta manipulation: %s, betaFactor: %s, avg fails: %s, minAvg %s, \
maxAvg %s, std deviation %s""" % 
(beta, betaManipulation, factor, avg, minAvg, maxAvg, stdDeviation))

        factor += 0.002
        betaManipulation = beta * factor


"""
Analysis for an Eblock nodes' distribution after a 
consecutive Byzantine primaries.
"""
def manipulationRepresenationAnalysis(nodesNum, byzantineNum, epoolSample, epoolSize, 
    txsInBlock, numConsecutiveByz):

    beta = epoolSample ** 2 - ((10/txsInBlock) ** (0.5))
    betaManipulation = beta * 1.1

    print("beta: %s, beta manipulation: %s" % (beta, betaManipulation))
    gamma = epoolSize / txsInBlock
    tau1 = (1-beta)/(gamma+beta-1)
    tau2 = (1-((1-beta)/gamma)**numConsecutiveByz)
    tau = tau1 * tau2

    print("gamma: %s, 2tau: %s" % (gamma, 2*tau))


    sim = simulator.FairnessSimulator(nodesNum, byzantineNum, epoolSample, epoolSize, 0)
    initialDist = sim.getGlobalEpoolDist()

    print(initialDist)

    dist = []
    for i in range(numConsecutiveByz):
        sim.allConstructValidEblocks(txsInBlock)
        manipulatedBlock = sim.byzantineManipulateItsBlock(betaManipulation)
        numFail = sim.validateEblocks(beta)

        if numFail < 3:
            sim.inputNewTxs(manipulatedBlock)
        else:
            print("Failed to pass the Eblock!")

        dist = sim.getGlobalEpoolDist()
        print(dist)

    
    distDiff = [abs(dist2-dist1) for dist1, dist2 in zip(initialDist, dist)]
    print("L^1 norm: %s" % (sum(distDiff)))
        

        


    
    
if __name__ == '__main__':
        
    #simulateEblockConstructionMethods(NODES_NUM, EPOOL_SAMPLE, EPOOL_SIZE, NUM_TX_IN_BLOCK)

    #manipulationAnalysis()

    manipulationRepresenationAnalysis(NODES_NUM, 1, EPOOL_SAMPLE, EPOOL_SIZE, 
        NUM_TX_IN_BLOCK, 10)
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 18 12:06:33 2018

@author: aviasayag
"""

import random



class Node:
    def __init__(self, index, sample):
        self.index = index
        self.portion = 0 # eblock portion
        self.sample = sample # global epool sample
        self.epool = []
        self.epoolSize = 0
        
        
"""
receive node lists and initalize their portions so it sums to 1
"""
def generateRandomPortions(nodesList):
    nodesNum = len(nodesList)
    randNums = []
    sum = 0
    
    for i in range(0, nodesNum):
        rand = random.random()
        sum += rand
        randNums.append(rand)
    
    for node in nodesList:
        node.portion = randNums[node.index]/sum
        
        

"""
Return nodes by the nodesNum and each node samples from the global epool by
the epoolSample (between 0 to 1). Furthermore each node contributes to the
global epool by a uniform distribution.
"""
def createNodes(nodesNum, epoolSample):
    nodesList = [];
    for n in range(0, nodesNum):
        newNode = Node(n, epoolSample)
        nodesList.append(newNode)
    
    generateRandomPortions(nodesList)
    return nodesList


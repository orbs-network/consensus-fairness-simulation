#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 13:11:12 2018

@author: aviasayag
"""


import transaction
import math
import random


"""
Each node from the nodesList is adding its own transactions (by its portion)
to the global-Epool. Returns the global epool
"""
def createGlobalEpool(nodesList, epoolSize):
    epool = []
    totalTxCreated = 0
    nodesNum = len(nodesList)
    
    for node in nodesList:
        txNum = math.floor(node.portion * epoolSize)
        totalTxCreated += txNum
        
        for i in range(txNum):
            epool.append(transaction.Transaction(node.index))
    
    # check if need to fill more transaction to reach EPOOL_SIZE
    txLeft = epoolSize - totalTxCreated
    
    if txLeft > 0:
        for i in range(txLeft):
            nodeIndex = i % nodesNum
            epool.append(transaction.Transaction(nodeIndex))
            
    return epool



"""
Each node chooses extra txs by its epoolSample
"""
def chooseTXs(nodesList, globalEpool):
    
    
    for node in nodesList:
        epoolSize = 0
        
        for epoolTx in globalEpool:
            
            # enter node's own txs
            if epoolTx.source == node.index:
                node.epool.append(epoolTx)
                epoolSize += 1
            else:
                # enter other nodes txs in probability
                if random.random() < node.sample:
                    node.epool.append(epoolTx)
                    epoolSize += 1
                
        node.epoolSize = epoolSize
        
        
"""
Get node and threshold and return all the txs from the node's epool that
their hash value is lower than the threshold
"""       
def sliceEpoolByThreshold(node, threshold):
    
    epool = node.epool
    slicedEpool = []
    
    
    for tx in epool:
        if tx.hashInt < threshold:
            slicedEpool.append(tx)
    
    return slicedEpool
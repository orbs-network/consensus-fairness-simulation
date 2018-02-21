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
EPOOL_SIZE = 10000

EPOOL_SAMPLE = 0.9 # num between 0 to 1
NUM_TX_IN_BLOCK = 500



if __name__ == '__main__':
        
    sim = simulator.Simulator(NODES_NUM, EPOOL_SAMPLE, EPOOL_SIZE, 1)
    
    sim.sim1(NUM_TX_IN_BLOCK)
    
    
    threshold = (NUM_TX_IN_BLOCK/9000) * (2**256)
    sim.sim2(NUM_TX_IN_BLOCK, threshold)
        
    sim.sim2B(threshold)
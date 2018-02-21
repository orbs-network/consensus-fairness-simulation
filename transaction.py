#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 18 11:59:35 2018

@author: aviasayag
"""


import random
import hashlib



class Transaction:
    def __init__(self, source):
        self.source = source
        self.data = random.random()
        self.hashInt = self.sha256ToInt()
    
    def __repr__(self):
        return "{Tx from %s with data %s}" % (self.source, self.data)
    
    def __hash__(self):
        return hash(self.source) ^ hash(self.data)
    
    def sha256(self):
        toHash = "%s,%s" % (self.source, self.data)
        return hashlib.sha256(toHash.encode())

    def sha256ToInt(self, addToBeginningOfHash=""):
        toHash = addToBeginningOfHash + "%s,%s" % (self.source, self.data)
        hashOut = hashlib.sha256(toHash.encode())
        return int(hashOut.hexdigest(), 16)
        

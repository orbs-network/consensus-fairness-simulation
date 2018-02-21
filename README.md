# Fairness Simulation

Simulation of multiple fairness methods in Eblock construction under high load epochs.

## Install

* Make sure you have Python 3.x.x (tested in Python 3.6.4). 

## Run

* To run a simulation create an instance of the Simulation class with the required simulation parameters (nodes_num, Epool_sample, Epool_size).

* Through the instance there are (as for now) 2 different Eblock construction methods where the rule for selecting transactions is:
    
    1. sim1: Choose all the transactions that their hash value is the smallest (SHA-256).

    2. sim2: Randomly choose transaction out of the set of transactions that their hash value is smaller than some threshold.


## Example

* Run main.py
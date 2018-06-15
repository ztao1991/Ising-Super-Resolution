# -*- coding: utf-8 -*-
"""
Created on Thu Jun 14 15:57:12 2018

@author: Stavros
"""

import numpy as np
from directories import mc_train_dir, mc_test_dir
from directories import mc_critical_train_dir, mc_critical_test_dir
from decimations import block_rg, block_rg_WD

## Temperature list for mc data ##
T_list = np.linspace(0.01, 4.538, 32)

################################################
########## DATA FOR TRAINING READERS  ##########
################################################

class TrainingData():
    def __init__(self, args):
        if args.CR:
            train_out = read_file_critical(L=args.L, n_samples=args.nTR, train=True)
            test_out = read_file_critical(L=args.L, n_samples=args.nTE, train=False)
        else:
            train_out = read_file(L=args.L, n_samples=args.nTR, train=True)
            test_out = read_file(L=args.L, n_samples=args.nTE, train=False)
        
        if args.RGWD:
            train_in = block_rg_WD(train_out)
            test_in = block_rg_WD(test_out)
        else:
            train_in = block_rg(train_out)
            test_in = block_rg(test_out)
        
        self.train_in, self.train_out = (add_index(train_in)[:args.TRS], 
                                         add_index(train_out)[:args.TRS])
        self.val_in, self.val_out = (add_index(test_in)[:args.VALS], 
                                     add_index(test_out)[:args.VALS])
        
        
###################################
########## LOAD MC DATA  ##########
###################################

def read_file(L=16, q=2, n_samples=10000, train=False):
    ## Returns dataset normilized to [0,1] ##
    if train:
        data = np.load(mc_train_dir%(n_samples, L, q))
    else:
        data = np.load(mc_test_dir%(n_samples, L, q))
    return data.reshape(data.shape[0], L, L)

def read_file_critical(L=16, n_samples=40000, train=False):
    if train:
        return np.load(mc_critical_train_dir%(n_samples, L))
    else:
        return np.load(mc_critical_test_dir%(n_samples, L))
    
####################################
########## DATA UTILITIES ##########
####################################

def add_index(data):
    ## Adds a 1-component dimension to a numpy array to use as input to CNN ##
    return data.reshape(data.shape+(1,))

def temp_partition(data, iT, n_samples=10000):
    return data[iT * n_samples : (iT+1) * n_samples]
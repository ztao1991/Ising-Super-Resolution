# -*- coding: utf-8 -*-
"""
Created on Mon Aug 13 22:23:40 2018

@author: Stavros
"""

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import gridspec
matplotlib.rcParams['mathtext.fontset'] = 'cm'
matplotlib.rcParams['font.family'] = 'STIXGeneral'
matplotlib.rcParams.update({'font.size': 36})

from plot_directories import T_list1D as T_list
from plot_directories import quantities_dir1D, quantities_dir1D_fixed
# Use this T_list when plot_directories module is not available
#T_list = np.linspace(0.01, 4.538, 32)


### !!! .NPY DESCRIPTION !!! ###
# obs = (32, 5, 12)
# ind1: temperatures
# ind2: [MC, RG, SR continuous, SR rounded, SR sampled]
# ind3: [Mag, En, Susc, specHeat, Mag2, Mag4, En2, tpf(L/2), 
#        tpf(L/4), S0, S1, S2]

# Load data (fix .npy directory here)
NAME = 'Simple1D32relu_L1_32_K53_PBC_MReg0.00EReg0.10B1000'
obs = np.load('%s/%s.npy'%(quantities_dir1D, NAME))

fixed_older = np.load('%s/Regular1D32relu_L1_20_MReg0.10EReg0.30B1000_gaussian_sampling.npy'%quantities_dir1D_fixed)

# Use rounding instead of sampling for the five lowest temperatures 
# to correct noise in susc and Cv
obs[:3, -1] = obs[:3, -2]

def plot_one(q=0, figsize=(8, 5), L=32):
    # q: which quantity to plot
    plt.figure(figsize=figsize)
    plt.plot(T_list, obs[:, 0, q], color='blue', label='%d MC'%L)
    plt.plot(T_list, obs[:, 1, q], '--', color='green', label='%d RG'%(L//2))
    plt.plot(T_list, obs[:, -1, q], 'x', color='red', label='%d SR'%L)
    
    plt.legend()
    
    plt.show()
    
def plot_four(qtot=4, figsize=(14, 8), L=32, save=False):
    # plots the four plots (M, E, chi, Cv)
    plt.figure(figsize=figsize)
    ylab = ['$M$', '$E$', '$\chi $', '$C_V$']
    for q in range(qtot):
        plt.subplot(221 + q)
        plt.plot(T_list, obs[:, 0, q], color='#ff0000', label='$N=$%d MC'%L,
                 linewidth=2.0)
        plt.plot(T_list, obs[:, 1, q], color='#e66464', 
                 label='$N=$%d RG'%(L//2), linewidth=2.0, alpha=0.6)
        
        plt.plot(T_list, obs[:, -1, q], 'o--', color='blue', label='$N=$%d SR'%L, linewidth=1.2)
        if q == 0:
            plt.legend()
        plt.xlabel('$T$')
        plt.ylabel(ylab[q])
        
        plt.locator_params(axis='y', nbins=5)
    
    if save:
        plt.savefig('%s.pdf'%NAME)
    else:
        plt.show()
        
fig = plt.figure(figsize=(20, 14))
# set height ratios for sublots
gs = gridspec.GridSpec(2, 1, height_ratios=[1, 1]) 

# the fisrt subplot
ax0 = plt.subplot(gs[0])
line_mcM, = ax0.plot(T_list, obs[:, 0, 0], color='#ff0000', linewidth=2.5)
line_rgM, = ax0.plot(T_list, obs[:, 1, 0], color='#e66464', linewidth=2.5, alpha=0.6)
line_srM, = ax0.plot(T_list, obs[:, -1, 0], 'o--', color='blue', linewidth=1.5)
plt.ylabel('$M$')

#the second subplot
ax1 = plt.subplot(gs[1], sharex = ax0)
line_mcE, = ax1.plot(T_list, obs[:, 0, 1], color='#ff0000', linewidth=2.5)
line_rgE, = ax1.plot(T_list, obs[:, 1, 1], color='#e66464', linewidth=2.5, alpha=0.6)
line_srE, = ax1.plot(T_list, obs[:, -1, 1], 'o--', color='blue', linewidth=1.5)
plt.setp(ax0.get_xticklabels(), visible=False)
plt.ylabel('$E$')

ax0.locator_params(axis='y', nbins=5)
ax1.locator_params(axis='y', nbins=5)
# remove last tick label for the second subplot
yticks = ax0.yaxis.get_major_ticks()
yticks[0].label1.set_visible(False)

# put lened on first subplot
ax0.legend((line_mcM, line_rgM, line_srM), ('$N=32$ MC', '$N=16$ RG', '$N=32$ SR'), loc='upper right')

plt.xlabel('$T$')
# remove vertical gap between subplots
plt.subplots_adjust(hspace=.0)
plt.savefig('%s.pdf'%NAME)
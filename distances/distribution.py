#!/usr/bin/env python3 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os
fsize=20

cols = ["distance1", "distance2", "distance3"] 
replicas = 1

def dframer(system, replicas):
    df = pd.DataFrame(columns=cols)
    for replica in range(1, replicas + 1):
        data = pd.read_csv(f'distances_{system}_r{replica}.dat', names = cols, delim_whitespace=True, skiprows=1) 
        df = pd.concat([df, data], ignore_index=True)
    return df

kde = True

colors = ['#a6cee3', '#b2df8a', '#f0027f', '#1f78b4', '#33a02c', '#fb9a99']


def plotter (system, replicas):
    plt.title(f'{system} distances distributions')
    df = dframer(system, replicas)
    for i, distance in enumerate(cols):
        ax = sns.kdeplot(df[distance], color = colors[i], fill=True)
        print(system)
        print(distance, df[distance].mean(), df[distance].std())
    plt.xlabel('Distance ($\AA$)', fontsize=fsize)
    ax.tick_params(labelsize=18)
#    plt.xlim(0.0,10.0)
#    plt.ylim(0.0,1.5)
    ax.legend(cols)
    plt.ylabel('Density', fontsize=fsize)
    plt.savefig(f'distributions_{system}.png')
    plt.show()

systems = ['WT']
for system in systems:
    plt.figure(figsize=(8,7))
    plotter(system, replicas)

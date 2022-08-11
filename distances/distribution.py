#!/usr/bin/env python3 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os
fsize=20

df= pd.read_csv('distances.dat', delim_whitespace=True) 

distances = df.columns
distances

kde = True

colors = ['#a6cee3', '#1f78b4', '#b2df8a', '#33a02c', '#fb9a99', '#f0027f']
#plt.xlim(0.0,18.0)
#plt.ylim(0.0,1.4)

plt.title('WT interactions ASP (3 us) Monomer A')
for i, distance in enumerate(distances):
    ax = sns.kdeplot(df[distance], color = colors[i], fill=True)
    print(distance, df[distance].mean(), df[distance].std())
plt.xlabel('Distance ($\AA$)', fontsize=fsize)
ax.tick_params(labelsize=18)
ax.legend(distances)
plt.ylabel('Density', fontsize=fsize)

plt.show()

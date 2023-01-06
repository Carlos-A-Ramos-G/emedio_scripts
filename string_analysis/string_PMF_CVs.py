#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os


PMF_FILE = 'system.PMF'
zero_in_PMF = 0.9243821816
#plot between s values
s_min = 0
s_max = 15

STRING_FILE = 'system.string'
numbers_of_CVs = 5
nodes = 96

fuente=15

reaction_pmf = pd.read_csv(PMF_FILE, \
                              delim_whitespace=True, names=['bin', 's', 'G'])
reaction_pmf['G_zeroed']  = reaction_pmf['G'] + zero_in_PMF
reaction_pmf= reaction_pmf[(reaction_pmf['s'] > s_min) & (reaction_pmf['s'] < s_max)]

CVs = pd.read_csv(STRING_FILE, delim_whitespace=True, names=[f'CV {i}' for i in range(1, numbers_of_CVs + 1)])
CVs['s'] = np.linspace(reaction_pmf['s'].min(), reaction_pmf['s'].max(), nodes)
CVs = CVs[(CVs['s'] >= 0)]


ax = plt.figure(figsize=(7,10))
plt.subplot(2,1,1)

sns.lineplot(x='s', y='G_zeroed', data= reaction_pmf, color='black')
plt.axhline(y = 0, color = 'g', linestyle = '-')
plt.ylabel('\u0394G ($kcal.mol^{-1}$)',fontsize=fuente)
plt.xlabel('s ($amu^{1/2}$$\AA$)',fontsize=fuente)
plt.yticks(fontsize=fuente)

#uncomment and modify accordingly to your needs
#plt.xticks(np.arange(0, 14, 2), fontsize=fuente)
#plt.xlim([-1, 14.0]) 

print(reaction_pmf['G_zeroed'].max()) # this will print the TS energy value

plt.subplot(2,1,2)


CVs = CVs.set_index('s')
#ax1 = sns.lineplot(data=CVs, linewidth=2.0, dashes=False)
ax1 = sns.lineplot(x='s' , y='CV 1', data= CVs, color='orange', linewidth=2.0)
ax1 = sns.lineplot(x='s' , y='CV 2', data= CVs, color='black', linewidth=2.0)
ax1 = sns.lineplot(x='s' , y='CV 3', data= CVs, color='green', linewidth=2.0)
ax1 = sns.lineplot(x='s' , y='CV 4', data= CVs, color='blue', linewidth=2.0)
ax1 = sns.lineplot(x='s' , y='CV 5', data= CVs, color='red', linewidth=2.0)
#ax1.get_legend().remove()
plt.xlabel('s ($amu^{1/2}$$\AA$)', fontsize=fuente)
plt.ylabel('Distances $\AA$', fontsize=fuente)
#uncomment and modify accordingly to your needs
#plt.yticks(np.arange(1, 4, 0.5), fontsize=fuente)
#plt.xticks(np.arange(0, 14, 2), fontsize=fuente)
#plt.xlim([-1, 14.0])
plt.yticks(fontsize=fuente)




sns.despine()
plt.savefig('acyl_WT_PMF_CVs.png', dpi = 300)
plt.tight_layout()
plt.show()

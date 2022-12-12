#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os

fuente=15
zero =  0.9243821816
s_min = -0.07
s_max = 13
PMF_file = 'system.PMF'
string_file = 'system.string'
CVs = 6
nodes = 96
acylation_pmf = pd.read_csv(PMF_file, \
                              delim_whitespace=True, names=['bin', 's', 'G'])
acylation_pmf['G_zeroed']  = acylation_pmf['G'] + zero
acylation_pmf= acylation_pmf[(acylation_pmf['s'] > s_min) & (acylation_pmf['s'] < s_max)]

CVs = pd.read_csv(string_file, delim_whitespace=True, names=[f'CV {i}' for i in range(1,CVs)])
CVs['s'] = np.linspace(acylation_pmf['s'].min(),acylation_pmf['s'].max(), nodes)
CVs = CVs[(CVs['s'] < s_max) & (CVs['s'] > s_min)]


ax = plt.figure(figsize=(7,10))
plt.subplot(2,1,1)

sns.lineplot(x='s', y='G_zeroed', data= acylation_pmf, color='black')
plt.axhline(y = 0, color = 'g', linestyle = '-')
plt.ylabel('\u0394G ($kcal.mol^{-1}$)',fontsize=fuente)
plt.xlabel('s ($amu^{1/2}$$\AA$)',fontsize=fuente)
plt.yticks(fontsize=fuente)
plt.xticks(np.arange(0, 14, 2), fontsize=fuente)
plt.xlim([-1, 14.0])


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
plt.yticks(np.arange(1, 4, 0.5), fontsize=fuente)
plt.xticks(np.arange(0, 14, 2), fontsize=fuente)
plt.xlim([-1, 14.0])
plt.yticks(fontsize=fuente)




sns.despine()
plt.savefig('system_PMF_CVs.png', dpi = 300)
plt.tight_layout()
plt.show()

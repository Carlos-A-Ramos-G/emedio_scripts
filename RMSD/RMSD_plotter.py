#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def rms_plotter(file, color):
    label = f'{file}'
    df = pd.read_csv(file, delim_whitespace=True, names=['frame', 'rmsd'], skiprows=8)
    df['time_us'] = df['frame']/10000
    sns.lineplot(x='time_us', y='rmsd', data= df, color=color, label=label)



replicas = 3
monomers = ['A', 'B']
molecules = ['Protein', 'Substrate']
#colors = ['#7fc97f', '#beaed4','#fdc086', '#ffff99', '#386cb0', '#f0027f', '#bf5b17', '#666666']
colors = ['#a6cee3', '#1f78b4', '#b2df8a', '#33a02c', '#fb9a99']

sns.set_context("paper", font_scale = 1.5)

plot = 0
plt.figure(figsize=(15,10))
for molecule in molecules:    
    for monomer in monomers:
        plt.subplot(len(molecules), len(monomers), plot+1)
        legends = []
        for replica in range(replicas):
            plt.title(f'{molecule} Heterodimer {monomer}')
            rms_plotter(f'R{replica+1}_rmsd_{molecule[0]}{monomer}.agr', colors[replica])
            legends.append(f'Replica {replica+1}')
        plt.legend(legends, loc=4)
        plt.xlabel('time (\u03BCs)')
        plt.ylabel('RMSD ($\AA$)')
        plot += 1
sns.despine()
plt.tight_layout()
plt.savefig('RMSD.png')
plt.show()

#!/usr/bin/env python3
import pandas as pd
import mdtraj as md
import matplotlib.pyplot as plt

t = md.load('traj.dcd', top='parm.prmtop')
#pair of atoms in distances numbering from zero
pairs = [[[80,2780]], 
        [[82, 2781]], 
        [[2010,83]]]

#compute the distances between pairs
def distance_measure(pairs):
    all_distances = []
    for pair in pairs:
        all_distances.append(md.compute_distances(t, pair)*10)
    
    
    #Save the distances to a file
    f = open('distances.dat', 'w')
    f.write('distance1   distance2   distance3\n')
    for i in range(t.n_frames):
        for j in range(len(all_distances)):
            f.write("{:<10f} ".format(all_distances[j][i][0]))
        f.write('\n')
    f.close()

def distance_plotter(file, pairs):
    cols = [f'Dist {i}' for i in range(1, len(pairs)+1)]
    df = pd.read_csv(file, names=cols, delim_whitespace=True)
    for col in cols:
        plt.plot(df[col])
    plt.title('distances along simulation')
    plt.legend(cols)
    plt.xlabel('time')
    plt.ylabel('$\AA$')
    plt.show()

#distance_measure(pairs)
distance_plotter('distances.dat', pairs)

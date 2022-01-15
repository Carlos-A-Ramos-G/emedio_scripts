#!/usr/bin/env python3
import mdtraj as md

t = md.load('traj.dcd', top='parm.prmtop')
#pair of atoms in distances numbering from zero
pairs = [[[80,2780]], [[82, 2781]], [[2010,83]]]

#compute the distances between pairs
all_distances = []
for pair in pairs:
    all_distances.append(md.compute_distances(t, pair)*10)


#Save the distances to a file
f = open('distances.dat', 'w')
for i in range(t.n_frames):
    for j in range(len(all_distances)):
        f.write("{:<10f} ".format(all_distances[j][i][0]))
    f.write('\n')
f.close()
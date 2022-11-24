#!/usr/bin/env python3
import numpy as np

WEIGHTS = [0.04064, 0.09032, 0.13031, 0.15617, 0.16512, 0.15617, 0.13031, 0.09032, 0.04064]
MODIFICATIONS = ['SYSTEM_NAME']
SYSTEMS = ['ligand','michaelis']


def get_filename(modification, system, replica, window):
    return f'{modification}/{system}/replica_{replica}/{window}/dvdl_{window}.dat'


def system_average(system, modification):
    averages = []
    for replica in range(1, 6):
        data = [np.loadtxt(get_filename(modification, system, replica, window)) for window in range(1, 10)]
        mean = np.dot(np.mean(data, axis=1), WEIGHTS)
        print(f'{system} replica {replica}: {mean:5.2f}')
        averages.append(mean)
    means = np.mean(averages)
    std = np.std(averages)
    print(f'mean for {system}: {means:5.2f} =/- {std:4.2f}')
    return means, std


def delta_delta_G(ligand, michaelis, modification):
    delta_G_ligand_mean, delta_G_ligand_std = system_average(ligand, modification)
    delta_G_michaelis_mean, delta_G_ligand_std = system_average(michaelis, modification)
    ddG = delta_G_michaelis_mean - delta_G_ligand_mean
    error = (delta_G_michaelis_std**2 + delta_G_ligand_std**2)**(1/2)
    print (f'ddG for {modification}: {ddG:5.2f} +/- {error:4.2f}')

delta_delta_G(SYSTEMS[0],SYSTEMS[1], MODIFICATIONS[0])

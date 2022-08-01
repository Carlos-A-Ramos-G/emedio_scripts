import mdtraj as md
import numpy as np
RES_INI = 100#int(input('ResIni: >'))
RES_FIN = 120#int(input('ResFin: >'))
traj = md.load('traj.nc', top = 'file.prmtop')

psi = md.compute_psi(traj)

resids = np.linspace(RES_INI, RES_FIN, RES_FIN - RES_INI + 1, dtype = 'int')
psi_interest = psi[1][:,RES_INI-2:RES_FIN-1]
psi_interest = psi_interest/np.pi*180

f = open("psi.txt", "w")

for res in resids:
    f.write("{:<10d} ".format(res))
f.write("\n")

for i in range(traj.n_frames):
    for j in range(len(resids)):
        f.write("{:<10.4f} ".format(psi_interest[i,j]))
    f.write("\n")
f.close()

phi = md.compute_phi(traj)

phi_interest = phi[1][:,RES_INI-2:RES_FIN-1]
phi_interest = phi_interest/np.pi*180

h = open("phi.txt", "w")

for res in resids:
    h.write("{:<10d} ".format(res))
h.write("\n")

for i in range(traj.n_frames):
    for j in range(len(resids)):
        h.write("{:<10.4f} ".format(phi_interest[i,j]))
    h.write("\n")
h.close()


PARM=parameters.prmtop
TRAJ=trajectory.nc
RESIDMASK=":1-278" #write here the resid of the protein and substrate
ANGLE=120
DISTANCE="3.2"



cpptraj <<EOF
parm $PARM
trajin $TRAJ 
hbond HBonds $RESIDMASK angle $ANGLE dist $DISTANCE  acceptormask ${RESIDMASK}&@N=,O=,S= solventdonor :WAT@O solventacceptor :WAT@O solvout solv.out bridgeout bridge.out avgout avg.out out number_hidrogen_bonds.out
run
quit
EOF


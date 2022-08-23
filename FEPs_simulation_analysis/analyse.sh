#!/bin/sh


WORKDIR=$(pwd)
for modification in `ls -d */`;do
    for system in ligand michaelis;do
        for replica in {1..5};do
            for window in {1..9};do
                grep L9 ${modification}/${system}/replica_${replica}/${window}/ti001_${window}.en | tail -n 4000 | awk '{print $6}' > ${modification}/${system}/replica_${replica}/${window}/dvdl_${window}.dat
                echo ${modification}/${system}/replica_${replica}/${window} done
            done
        done
    done
done
python3.6 FEP_gaussian_quadrature_integrator.py

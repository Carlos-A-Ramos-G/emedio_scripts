#!/bin/bash
#SBATCH --job-name=pbi_r1_NC
#SBATCH --output=mpi_%j.out
#SBATCH --error=mpi_%j.err
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=40
#SBATCH --ntasks-per-node=1
#SBATCH --ntasks-per-socket=1
#SBATCH --gres=gpu:1

module load atlas/3.10.3 python/2.7.14 amber/18

DIR=$(pwd)

cd $DIR/00_prep
tleap -f leap_pbi0451

cd $DIR/01_min
pmemd.cuda -O -i min.in  -o sytem_name_min_1.out -p ../00_prep/sytem_name.prmtop -c ../00_prep/sytem_name.inpcrd -r sytem_name_min_1.rst -ref ../00_prep/sytem_name.inpcrd
for i in `seq 11 100`;do 
    pmemd.cuda -O -i min.in  -o sytem_name_min_${i}.out -p ../00_prep/sytem_name.prmtop -c sytem_name_min_$((i-1)).rst -r sytem_name_min_${i}.rst -ref sytem_name_min_$((i-1)).rst
done

cd $DIR/02_heat
cp ../01_min/sytem_name_min_100.rst  sytem_name_heat_0.rst
for i in {1..3};do
	srun pmemd.cuda -O -i heat.in -o sytem_name_heat_${i}.out -p ../00_prep/sytem_name.prmtop -c sytem_name_heat_$((i-1)).rst -r sytem_name_heat_${i}.rst -x sytem_name_heat_${i}.nc -ref sytem_name_heat_$((i-1)).rst
done

cd $DIR/03_equil
srun pmemd.cuda -O -i equil_15.0.in -o sytem_name_equil_1.out -p ../00_prep/sytem_name.prmtop -c ../02_heat/sytem_name_heat_3.rst -r sytem_name_equil_1.rst -x sytem_name_equil_1.nc -ref ../02_heat/sytem_name_heat_3.rst
srun pmemd.cuda -O -i equil_12.0.in -o sytem_name_equil_2.out -p ../00_prep/sytem_name.prmtop -c sytem_name_equil_1.rst -r sytem_name_equil_2.rst -x sytem_name_equil_2.nc -ref sytem_name_equil_1.rst 
srun pmemd.cuda -O -i equil_9.0.in -o sytem_name_equil_3.out -p ../00_prep/sytem_name.prmtop -c sytem_name_equil_2.rst -r sytem_name_equil_3.rst -x sytem_name_equil_3.nc -ref sytem_name_equil_2.rst 
srun pmemd.cuda -O -i equil_6.0.in -o sytem_name_equil_4.out -p ../00_prep/sytem_name.prmtop -c sytem_name_equil_3.rst -r sytem_name_equil_4.rst -x sytem_name_equil_4.nc -ref sytem_name_equil_3.rst
srun pmemd.cuda -O -i equil_3.0.in -o sytem_name_equil_5.out -p ../00_prep/sytem_name.prmtop -c sytem_name_equil_4.rst -r sytem_name_equil_5.rst -x sytem_name_equil_5.nc -ref sytem_name_equil_4.rst 
srun pmemd.cuda -O -i equil_free.in -o sytem_name_equil_6.out -p ../00_prep/sytem_name.prmtop -c sytem_name_equil_5.rst -r sytem_name_equil_6.rst -x sytem_name_equil_6.nc

cd $DIR/04_NVT
srun pmemd.cuda -O -i prod.in -o sytem_name_NVT_1.out -p ../00_prep/sytem_name.prmtop -c ../03_equil/sytem_name_equil_6.rst -r sytem_name_NVT_1.rst -x sytem_name_NVT_1.nc 
sh script.sh

for i in `seq 2 5`;do
sed  -e "s/{pasado}/"$((i-1))"/g" -e "s/{presente}/"$i"/g" -e "s/{futuro}/"$((i+1))"/g"  run_template > run${i}.cmd
done
#sbatch run2.cmd 

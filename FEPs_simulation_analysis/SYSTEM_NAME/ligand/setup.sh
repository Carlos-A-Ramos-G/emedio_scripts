top=$(pwd)
setup_dir=$top/../setup

RESI="':1'"  #TIMASK1
SCMASK1="'@15-17'" 
RESF="':2'"	#TIMASK2
SCMASK2="'@32-35'"
RESNEW=MHSP

AMBERver=20
PARAMETERS=ligands_solvated.prmtop
COORDINATES=ligands_solvated.inpcrd
for replica in {1..5};do
    COUNTER=0
    for w in 0.01592 0.08198 0.19331 0.33787 0.5 0.66213 0.80669 0.91802 0.98408; do
        COUNTER=$((COUNTER+1))
        mkdir -p $top/replica_${replica}/$COUNTER
        sed -e "s/XXXX/${w}/g" \
            -e "s/RESI/$RESI/g" \
            -e "s/RESF/$RESF/g" \
            -e "s/SCMASK1/$SCMASK1/g" \
            -e "s/SCMASK2/$SCMASK2/g" $top/prod > $top/replica_${replica}/$COUNTER/ti_${COUNTER}.in
        cd $top/replica_${replica}/$COUNTER	
        (
    	ln -sf $setup_dir/$PARAMETERS ti.prmtop
    	ln -sf $setup_dir/$COORDINATES ti.inpcrd
        )
    done
    cd $top 
    COUNTER=0
    for w in 0.01592 0.08198 0.19331 0.33787;do
        COUNTER=$((COUNTER+1))
        sed -e "s/RESNEW/${RESNEW}/g" \
            -e "s/AMBERver/${AMBERver}/g" \
            -e "s/PRESENT/${COUNTER}/g" \
            -e "s/PAST/$((COUNTER-1))/g" \
            -e "s/FUTUR/$((COUNTER+1))/g" \
            -e "s#REPLICA#$replica#g" $top/FEP_GPU1to4 > $top/replica_${replica}/$COUNTER/FEP_PROD_${COUNTER}.cmd
    done
    
    COUNTER=$((COUNTER+1))
    sed -e "s/RESNEW/${RESNEW}/g" \
        -e "s/AMBERver/${AMBERver}/g" \
        -e "s#PRESENT#${COUNTER}#g" \
        -e "s#PAST#$top/replica_${replica}/$((COUNTER-1))#g" \
        -e "s#FUTUR#$top/replica_${replica}/$((COUNTER+1))#g" \
        -e "s#REPLICA#$replica#g" $top/FEP_GPU5 > $top/replica_${replica}/$COUNTER/FEP_PROD_${COUNTER}.cmd
    sed -e "s/XXXX/0.5/g" -e "s/RESI/$RESI/g" \
        -e "s/RESF/$RESF/g" \
        -e "s/SCMASK1/$SCMASK1/g" \
        -e "s/SCMASK2/$SCMASK2/g" $top/min > $top/min.in
    sed -e "s/XXXX/0.5/g" \
        -e "s/RESI/$RESI/g" \
        -e "s/RESF/$RESF/g" \
        -e "s/SCMASK1/$SCMASK1/g" \
        -e "s/SCMASK2/$SCMASK2/g" $top/equil > $top/equil.in
    sed -e "s/RESNEW/${RESNEW}/g" \
        -e "s/AMBERver/${AMBERver}/g" FEP_CPU_equil >  $top/FEP_EQUIL.cmd
    sed -e "s/RESNEW/${RESNEW}/g" \
        -e "s/AMBERver/${AMBERver}/g" FEP_MIN >  $top/FEP_MIN.cmd
    ln -sf $setup_dir/$PARAMETERS ti.prmtop
    ln -sf $setup_dir/$COORDINATES ti.inpcrd
    
    for w in 0.66213 0.80669 0.91802 0.98408;do
        COUNTER=$((COUNTER+1))
        sed -e "s/RESNEW/${RESNEW}/g" \
            -e "s/AMBERver/${AMBERver}/g" \
            -e "s/PRESENT/${COUNTER}/g" \
            -e "s/PAST/$((COUNTER-1))/g" \
            -e "s/FUTUR/$((COUNTER+1))/g" \
            -e "s#REPLICA#$replica#g" $top/FEP_GPU6to9 > $top/replica_${replica}/$COUNTER/FEP_PROD_${COUNTER}.cmd
    done
done


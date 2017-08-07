#!/bin/bash

let numjobs=$1
echo "Spawning ${numjobs} jobs"

SINGULARITY_IMG=/mnt/sdb/larbys/containers/singularity-dllee-unified-072517.img
WORKDIR=/home/taritree/dllee_integration/dllee-tufts-slurm/
TAGGER_CFG=${WORKDIR}/tagger.cfg
INPUTLISTS=${WORKDIR}/inputlists
OUTDIR=/mnt/sdb/larbys/data/comparison_samples/1mu1p/out_week080717/tagger
JOBIDLIST=${WORKDIR}/rerunlist.txt

rm -f log_mccaffery_job.txt
for (( i=0; i<$numjobs; i++ ))
do
    #SLURM_PROCID=$i ./mccaffe_test.sh &
    echo "launching job=$i" && nohup nice -n 10 singularity exec -B /mnt/sdb:/mnt/sdb $SINGULARITY_IMG bash -c "export SLURM_PROCID=$i && cd ${WORKDIR} && source run_job.sh ${TAGGER_CFG} ${INPUTLISTS} ${OUTDIR} ${JOBIDLIST}" >> log_mccaffery_job.txt 2>&1 &
done

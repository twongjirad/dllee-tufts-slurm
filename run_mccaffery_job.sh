#!/bin/bash

let numjobs=$1
echo "Spawning ${numjobs} jobs"

SINGULARITY_IMG=/home/taritree/larbys/images/dllee_unified/singularity-dllee-unified-062517.img
WORKDIR=/home/taritree/dllee_integration/dllee-tufts-slurm/
TAGGER_CFG=${WORKDIR}/tagger.cfg
INPUTLISTS=${WORKDIR}/inputlists
OUTDIR=/home/taritree/larbys/data/mcc8.1/nue_1eNpfiltered/out_week0625/tagger/
JOBIDLIST=${WORKDIR}/jobidlist.txt

rm -f log_mccaffery_job.txt
for (( i=0; i<$numjobs; i++ ))
do
    #SLURM_PROCID=$i ./mccaffe_test.sh &
    echo "launching job=$i" && singularity exec $SINGULARITY_IMG bash -c "export SLURM_PROCID=$i && cd ${WORKDIR} && source run_job.sh ${TAGGER_CFG} ${INPUTLISTS} ${OUTDIR} ${JOBIDLIST}" >> log_mccaffery_job.txt &
done

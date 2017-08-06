#!/bin/bash

# Used to run sort_comparison_samples.py
# That script is used to group larcv and larlite files from the comparison samples data set

CONTAINER=/cluster/kappa/90-days-archive/wongjiradlab/larbys/images/dllee_unified/singularity-dllee-unified-072517.img
#WORKDIR=/cluster/kappa/90-days-archive/wongjiradlab/larbys/data/comparison_samples/1e1p/
WORKDIR=/cluster/kappa/90-days-archive/wongjiradlab/grid_jobs/dllee-tufts-slurm

module load singularity

singularity exec ${CONTAINER} bash -c "source /usr/local/bin/thisroot.sh && cd /usr/local/share/dllee_unified && source configure.sh && cd ${WORKDIR} && python sort_comparison_samples.py"


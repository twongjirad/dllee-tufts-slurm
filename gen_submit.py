import os,sys

PARTITIONS=10

submit="""#!/bin/bash
#
#SBATCH --job-name=tag%02d
#SBATCH --output=log_tagger_extbnb_p%02d.txt
#SBATCH --ntasks=100
#SBATCH --time=90:00
#SBATCH --mem-per-cpu=2400

WORKDIR=/cluster/kappa/90-days-archive/wongjiradlab/grid_jobs/dllee-tufts-slurm
# tagger version 1 for nov review
CONTAINER=/cluster/kappa/90-days-archive/wongjiradlab/larbys/images/dllee_unified/singularity-dllee-unified-072517.img
# tagger version 2
#CONTAINER=/cluster/kappa/90-days-archive/wongjiradlab/larbys/images/dllee_unified/singularity-dllee-unified-20171013.img
JOBIDLIST=${WORKDIR}/rerunlist_p%02d.txt

# Tagger v1 configs
# -----------------
# For MC
#CONFIG=${WORKDIR}/tagger.cfg
# For Data
CONFIG=${WORKDIR}/tagger_data.cfg

# Tagger v2 configs
# -----------------
# For MC
#CONFIG=${WORKDIR}/taggermc_v2.cfg

INPUTLISTDIR=${WORKDIR}/inputlists

#OUTPUTDIR=/cluster/kappa/90-days-archive/wongjiradlab/larbys/data/comparison_samples/1e1p/out_week101317/tagger
#OUTPUTDIR=/cluster/kappa/90-days-archive/wongjiradlab/larbys/data/comparison_samples/inclusive_muon/out_week080717/tagger
#OUTPUTDIR=/cluster/kappa/90-days-archive/wongjiradlab/larbys/data/comparison_samples/ncpizero/out_week080717/tagger
#OUTPUTDIR=/cluster/kappa/90-days-archive/wongjiradlab/larbys/data/comparison_samples/extbnb/out_week082817/tagger
#OUTPUTDIR=/cluster/kappa/90-days-archive/wongjiradlab/larbys/data/comparison_samples/corsika/out_week082817/tagger
OUTPUTDIR=/cluster/kappa/90-days-archive/wongjiradlab/larbys/data/comparison_samples/extbnb_wprecuts_reprocess/out_week10132017/tagger_p04
#OUTPUTDIR=/cluster/kappa/90-days-archive/wongjiradlab/larbys/data/bnbdata_5e19/out_week082817/tagger

mkdir -p ${OUTPUTDIR}
module load singularity
srun singularity exec ${CONTAINER} bash -c "cd ${WORKDIR} && source run_job.sh ${CONFIG} ${INPUTLISTDIR} ${OUTPUTDIR} ${JOBIDLIST}"
"""

for p in range(PARTITIONS):
    s = open("submit_p%02d.sh"%(p),'w')
    print >>s,submit%(p,p,p)
    s.close()

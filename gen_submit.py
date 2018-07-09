import os,sys

PARTITIONS=10

submit="""#!/bin/bash
#
#SBATCH --job-name=tag%02d
#SBATCH --output=log_tagger_cocktail_p%02d.txt
#SBATCH --ntasks=%d
#SBATCH --time=540:00
#SBATCH --mem-per-cpu=2400

WORKDIR=/cluster/kappa/90-days-archive/wongjiradlab/grid_jobs/dllee-tagger-scripts
# tagger version 1 for nov review
#CONTAINER=/cluster/kappa/90-days-archive/wongjiradlab/larbys/images/dllee_unified/singularity-dllee-unified-072517.img
# tagger version 2
#CONTAINER=/cluster/kappa/90-days-archive/wongjiradlab/larbys/images/dllee_unified/singularity-dllee-unified-20171013.img
CONTAINER=/cluster/kappa/90-days-archive/wongjiradlab/larbys/images/dllee_unified/singularity-dllee-unified-taggerv2alpha-20171121.img
JOBIDLIST=${WORKDIR}/rerunlist_p%02d.txt

# Tagger v1 configs
# -----------------
# For MC
#CONFIG=${WORKDIR}/tagger.cfg
# For Data
#CONFIG=${WORKDIR}/tagger_data.cfg

# Tagger v2 configs
# -----------------
# For MC
#CONFIG=${WORKDIR}/taggermc_v2.cfg
# For MC, truth reco study
#CONFIG=${WORKDIR}/tagger_mctruth_study.cfg
# For Data,
CONFIG=${WORKDIR}/tagger_data_v2_splity.cfg

INPUTLISTDIR=${WORKDIR}/inputlists

OUTPUTDIR=/cluster/kappa/90-days-archive/wongjiradlab/larbys/data/bnbdata_5e19/out_week112117/tagger_v2alpha_fixedcroisplity

mkdir -p ${OUTPUTDIR}
module load singularity
srun singularity exec ${CONTAINER} bash -c "cd ${WORKDIR} && source run_job.sh ${CONFIG} ${INPUTLISTDIR} ${OUTPUTDIR} ${JOBIDLIST}"
"""

for p in range(PARTITIONS):
    rerunlistname = "rerunlist_p%02d.txt"%(p) 
    if not os.path.exists(rerunlistname):
        continue
    runlist = open(rerunlistname,'r')
    njobs = len(runlist.readlines())
    runlist.close()
    s = open("submit_p%02d.sh"%(p),'w')
    print >>s,submit%(p,p,njobs,p)
    s.close()

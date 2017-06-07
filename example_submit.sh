#!/bin/bash
#
#SBATCH --job-name=tagger
#SBATCH --output=tagger_log.txt
#
#SBATCH --ntasks=3
#SBATCH --time=20:00
#SBATCH --mem-per-cpu=4000


module load singularity
#srun singularity exec /cluster/kappa/90-days-archive/wongjiradlab/larbys/images/dllee_unified/twongjirad-singularity-dllee-ubuntu-master.img bash -c "cd ~/grid_jobs/ && source run_job.sh /cluster/home/twongj01/grid_jobs/tagger.cfg /cluster/kappa/90-days-archive/wongjiradlab/larbys/slurm/tagger/inputlists /cluster/kappa/90-days-archive/wongjiradlab/larbys/data/out/mcc8numu /cluster/kappa/90-days-archive/wongjiradlab/larbys/slurm/tagger/jobidlist.txt"

srun singularity exec /cluster/kappa/90-days-archive/wongjiradlab/larbys/images/dllee_unified/twongjirad-singularity-dllee-ubuntu-master.img bash -c "cd /cluster/home/twongj01/grid_jobs/ && source run_job.sh /cluster/home/twongj01/grid_jobs/tagger.cfg /cluster/home/twongj01/grid_jobs/inputlists /cluster/kappa/90-days-archive/wongjiradlab/larbys/data/out/mcc8numu /cluster/home/twongj01/grid_jobs/jobidlist.txt"

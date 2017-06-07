import os, sys

template="""#!/bin/bash
#
#SBATCH --job-name=__JOBNAME__
#SBATCH --output=__JOBNAME___log.txt
#
#SBATCH --ntasks=3
#SBATCH --time=20:00
#SBATCH --mem-per-cpu=4000


module load singularity

srun singularity exec /cluster/kappa/90-days-archive/wongjiradlab/larbys/images/dllee_unified/__IMAGENAME__ bash -c "cd /cluster/home/__TUNAME__/__SCRIPTSDIR__/ && source run_job.sh /cluster/home/__TUNAME__/__SCRIPTSDIR__/tagger.cfg /cluster/home/__TUNAME__/__SCRIPTSDIR__/inputlists /cluster/kappa/90-days-archive/wongjiradlab/__OUTDIR__ /cluster/home/__TUNAME__/__SCRIPTSDIR__/jobidlist.txt"
"""


def gen_submit_tagger_script( tufts_user_name, image_name, scriptdir, outdir, jobname="tagger" ):
    tagger_submit_script = template.replace("__TUNAME__",tufts_user_name)
    tagger_submit_script = tagger_submit_script.replace("__IMAGENAME__", image_name)
    tagger_submit_script = tagger_submit_script.replace("__SCRIPTSDIR__", scriptdir)
    tagger_submit_script = tagger_submit_script.replace("__JOBNAME__", jobname)
    tagger_submit_script = tagger_submit_script.replace("__OUTDIR__", outdir)
    out = open("submit.sh",'w')
    print >> out, tagger_submit_script
    out.close()



if __name__=="__main__":

    if len(sys.argv)!=4:
        print "usage: python gen_submit_tagger_script.py [image name] [outdir] [jobname]"
        sys.exit(-1)

    pworkdir = os.popen("pwd")
    workdir = pworkdir.readlines()[0]
    pwhoami  = os.popen("whoami")
    user = pwhoami.readlines()[0].strip()
    
    scriptdir = workdir.strip().split("/")[-1]
    
    if len(workdir.strip().split("/"))!=5 or workdir.strip().split("/")[1]!="cluster" or workdir.strip().split("/")[2]!="home" or workdir.strip().split("/")[3]!=user:
        print "This script was meant to run in /cluster/home/%s/[folder container in this script]" % ( user )
        sys.exit(-1)

    image_name = sys.argv[1]
    outdir = sys.argv[2]
    job_name  = sys.argv[3]

    outpath = "/cluster/kappa/90-days-archive/wongjiradlab/__OUTDIR__"
    outpath = outpath.replace("__OUTDIR__",outdir)

    if not os.path.exists( outpath ):
        print "Could not find output dir: ",outpath
        sys.exit(-1)

    gen_submit_tagger_script( user, image_name, scriptdir, outdir, job_name )
        



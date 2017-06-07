# dllee-tufts-slurm

This folder contains script templates for running the DL LEE Singularity container on the Tufts cluster.

# Instructions

## Building the container

You will need to build and prepare the DL LEE container you wish to run. Follow [these]() instructions to do so.

Once ready you should put the container here:

    /cluster/kappa/90-days-archive/wongjiradlab/larbys/images/dllee_unified/

(Don't forget to copy the photon library data file to right location, `/usr/local/share/dllee_unified/larlite/UserDev/SelectionTool/OpT0Finder/PhotonLibrary/dat`.)

## Preparing to run

First, clone this repository to your home space:

    git clone https://github.com/twongjirad/dllee-tufts-slurm


Next, go into `make_inputlists.py` and set the LARCV and LARLITE input folders. For example, the location for MCC8 numu+cosmic input files are at

    LARCV_SOURCE="/cluster/kappa/90-days-archive//wongjiradlab/larbys/data/mcc8/calmod_mcc8_bnb_nu_cosmic_v06_26_01_run01.09000_run01.09399_v01_p00_out"
    LARLITE_SOURCE="/cluster/kappa/90-days-archive/wongjiradlab/larbys/data/mcc8/calmod_mcc8_bnb_nu_cosmic_v06_26_01_run01.09000_run01.09399_v01_p00_out"

This will fill the `inputlists` folder with files that tell the tagger where to find the input files for job X. It also produces `jobidlist.txt`, which maps the `SLURM_PROCID` to the job ID.

Next, generate the submission script

    python gen_submit_tagger_script.py [image name] [outdir] [job name]

The arguments are

* `[image name]`: name of the DL LEE Singularity container you made
* `[out dir]`: relative path from the `wongjiradlab` folder `/cluster/kappa/90-days-archive/wongjiradlab`. An example would be `larbys/data/out/mcc8numu`
* `[job name]`: whatever you want to call this job, e.g. `tagger`

For an example of a fully-formed script, see `example_submit.sh`.

Now go into `submit.sh` and modify the `SBATCH` parameters, which control how the job is run. Some parameters

* `--ntasks=N`: this is the number of jobs to run
* `--time=HH:MM:SS`: estimated max duration. Once a job runs for this duratinon, it is killed. The default value (if not set) is very short, 5 minutes.
* `--mem-per-cpu`: amount of memory each CPU (job) is provided

## Submitting

To submit the job, run

    sbatch submit.sh

That's it.

To check the status, use

    squeue -u [user name]


The `run_job.sh` script is set to send errors and standard out to

     /cluster/home/[user name]/[repo folder]/slurm_tagger_[jobid]/log_[jobid].txt

To check this you can use something like

    tail -n 50 /cluster/home/[user name]/[repo folder]/slurm_tagger_[jobid]/log_[jobid].txt


## Performance Plots

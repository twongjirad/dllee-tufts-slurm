#!/bin/sh

# REMEMBER, WE ARE IN THE CONTAINER RIGHT NOW
# This means we access the next work drives through some mounted folders

export DLLEE_UNIFIED_BASEDIR=/usr/local/share/dllee_unified

source /usr/local/bin/thisroot.sh
source /usr/local/share/dllee_unified/configure.sh

echo "CURRENT DIR: "$PWD

tagger_cfg_path=$1
inputlist_dir=$2
output_dir=$3
jobid_list=$4


let NUM_PROCS=`cat ${jobid_list} | wc -l`
echo "number of processes: $NUM_PROCS"
if [ "$NUM_PROCS" -lt "${SLURM_PROCID}" ]; then
    echo "No Procces ID to run."
    return
fi

let "proc_line=${SLURM_PROCID}+1"
echo "sed -n ${proc_line}p ${jobid_list}"
let jobid=`sed -n ${proc_line}p ${jobid_list}`
echo "JOBID ${jobid}"

slurm_folder=`printf slurm_tagger_job%04d ${jobid}`
mkdir -p ${slurm_folder}
cd ${slurm_folder}/

# copy over input list
inputlist_larcv=`printf ${inputlist_dir}/input_larcv_%04d.txt ${jobid}`
inputlist_larlite=`printf ${inputlist_dir}/input_larlite_%04d.txt ${jobid}`

cp $inputlist_larcv input_larcv.txt
cp $inputlist_larlite input_larlite.txt
cp $tagger_cfg_path tagger_wire.cfg

ls -lh

# ./run_tagger [cfg]
logfile=`printf log_%04d.txt ${jobid}`
run_tagger tagger_wire.cfg >& logfile

outfile_larcv=`printf ${output_dir}/taggerout_larcv_%04d.root ${jobid}`
outfile_larlite=`printf ${output_dir}/taggerout_larlite_%04d.root ${jobid}`
cp tagger_anaout_larcv.root $outfile_larcv
cp tagger_anaout_larlite.root $outfile_larlite

# clean up
#cd ../
#rm -r $slurm_folder

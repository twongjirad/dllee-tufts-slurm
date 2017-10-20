import os,sys
import ROOT as rt

TUFTS="/cluster/kappa/90-days-archive/wongjiradlab/larbys/data"
MCCAFFREY="/mnt/sdb/larbys/data"
#MCCAFFREY="/home/taritree/larbys/data2"
DATAFOLDER="__unset__"
try:
    LOCAL_MACHINE=os.popen("uname -n").readlines()[0].strip()
    if LOCAL_MACHINE not in ["mccaffrey","login001"]:
        raise RuntimeError("unrecognized machine")

    if LOCAL_MACHINE=="mccaffrey":
        DATAFOLDER=MCCAFFREY
    elif LOCAL_MACHINE=="login001":
        DATAFOLDER=TUFTS
        
except:
    print "Could not get machine name"
    LOCAL_MACHINE=os.popen("uname -n").readlines()
    print LOCAL_MACHINE
    sys.exit(-1)

if DATAFOLDER=="__unset__":
    raise RuntimeError("Didnt set DATAFOLDER properly.")

exclude_running = True
clear_good_jobs = True

# Check job id list. Check output folder. Check that tagger output files have entries (and same number of entries)
# based on checks, will produce rerun list

# MCC8.1 MC corsika cosmics: mccaffrey
#TAGGER_FOLDER="/home/taritree/larbys/data/mcc8.1/corsika_mc/out_week0626/tagger"

# MCC8.1 nue+cosmic: tufts
#TAGGER_FOLDER="/cluster/kappa/90-days-archive/wongjiradlab/larbys/data/mcc8.1/nue_1eNpfiltered/out_week072517/tagger"

# MCC8.1 nue+cosmics: maccaffery
#TAGGER_FOLDER="/home/taritree/larbys/data/mcc8.1/nue_1eNpfiltered/out_week0626/tagger"

# MCC8.1 nue only: tufts
#TAGGER_FOLDER="/cluster/kappa/90-days-archive/wongjiradlab/larbys/data/mcc8.1/nue_nocosmic_1eNpfiltered/out_week0626/tagger"

# MCC8.1 numu+cosmic: tufts
#TAGGER_FOLDER="/cluster/kappa/90-days-archive/wongjiradlab/larbys/data/mcc8.1/numu_1muNpfiltered/out_week071017/tagger"

# MCC8.1 corsika cosmic MC: tufts
#TAGGER_FOLDER="/cluster/kappa/90-days-archive/wongjiradlab/larbys/data/mcc8.1/corsika_mc2/out_week071017/tagger"

# Comparison Samples
# ------------------

# 1e1p nue+cosmics: Tufts
#TAGGER_FOLDER=DATAFOLDER+"/comparison_samples/1e1p/out_week080717/tagger"

# 1mu1p nue+cosmics: McCaffrey
#TAGGER_FOLDER=DATAFOLDER+"/comparison_samples/1mu1p/out_week080717/tagger"

# BNB numu inclusive
#TAGGER_FOLDER=DATAFOLDER+"/comparison_samples/inclusive_muon/out_week080717/tagger"

# NCpi0
#TAGGER_FOLDER=DATAFOLDER+"/comparison_samples/ncpizero/out_week080717/tagger"

# EXTBNB w/ precuts
#TAGGER_FOLDER=DATAFOLDER+"/comparison_samples/extbnb/out_week082817/tagger"
#TAGGER_FOLDER=DATAFOLDER+"/comparison_samples/extbnb_wprecuts/out_week082817/tagger"
TAGGER_FOLDER=DATAFOLDER+"/comparison_samples/extbnb_wprecuts_reprocess/out_week10132017/tagger_p03"

# Corsika w/ precuts
#TAGGER_FOLDER=DATAFOLDER+"/comparison_samples/corsika/out_week082817/tagger"

# BNB DATA, 5e19 sample
#TAGGER_FOLDER=DATAFOLDER+"/bnbdata_5e19/out_week082817/tagger"



files = os.listdir(TAGGER_FOLDER)

file_dict = {}
for f in files:
    f.strip()
    idnum = int(f.split("_")[-1].split(".")[0])
    if idnum not in file_dict:
        file_dict[idnum] = {"larcv":None,"larlite":None}
    if "larcv" in f:
        file_dict[idnum]["larcv"] = TAGGER_FOLDER+"/"+f
    elif "larlite" in f:
        file_dict[idnum]["larlite"] = TAGGER_FOLDER+"/"+f

ids = file_dict.keys()
ids.sort()

# get list of ids of slurm jobs in the directory
jobidlist = []
workdir_list = os.listdir(".")
for f in workdir_list:
    f = f.strip()
    if "slurm_tagger_job" not in f:
        continue
    jobid = int(f.split("job")[-1])
    jobidlist.append(jobid)
print "JobIDs that might be running: ",len(jobidlist)

rerun_list = []
good_list = []
for fid in ids:
    try:
        rfile_larcv = rt.TFile( file_dict[fid]["larcv"] )
        tree = rfile_larcv.Get("image2d_modimg_tree")
        nentries_larcv = tree.GetEntries()
        rfile_larcv.Close()
                
        rfile_larlite = rt.TFile( file_dict[fid]["larlite"] )
        tree = rfile_larlite.Get("larlite_id_tree")
        nentries_larlite = tree.GetEntries()
        rfile_larlite.Close()
        if nentries_larcv!=nentries_larlite or nentries_larcv==0 or nentries_larlite==0:
            raise runtime_error("not the same")
        good_list.append(fid)
    except:
        rerun_list.append(fid)
        continue

print "Goodlist: ",len(good_list)
print "Rerunlist: ",len(rerun_list)

# read in jobidlist
fjobid = open("jobidlist.txt",'r')
ljobid = fjobid.readlines()
njobstot = 0
for l in ljobid:
    jobid = int(l.strip())
    njobstot += 1
    if jobid in good_list or jobid in rerun_list or (exclude_running and jobid in jobidlist):
        # remove folders for good ids
        if jobid in good_list:
            print "Jobid ",jobid," is good."
            if clear_good_jobs:
                os.system("rm -rf slurm_tagger_job%d"%(jobid))
        continue
    else:
        rerun_list.append(jobid)
fjobid.close()

print "Total Jobs: ",njobstot

print "Remaining list: ",len(rerun_list)

frerun = open("rerunlist.txt",'w')
for jobid in rerun_list:
    print >> frerun,jobid
frerun.close()

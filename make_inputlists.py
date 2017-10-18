import os,sys

# SPECIFY FOLDER WHERE INPUT DATA LIVES
# ------------------------------------------------------------------------
TUFTS="/cluster/kappa/90-days-archive/wongjiradlab/larbys/data"
MCCAFFREY="/mnt/sdb/larbys/data"
DAVIS="/media/data/larbys/data"
DATAFOLDER="__unset__"
try:
    LOCAL_MACHINE=os.popen("uname -n").readlines()[0].strip()
    if LOCAL_MACHINE not in ["mccaffrey","login001","davis"]:
        raise RuntimeError("unrecognized machine: %s"%(LOCAL_MACHINE))

    if LOCAL_MACHINE=="mccaffrey":
        DATAFOLDER=MCCAFFREY
    elif LOCAL_MACHINE=="login001":
        DATAFOLDER=TUFTS
    elif LOCAL_MACHINE=="davis":
        DATAFOLDER=DAVIS
        
except:
    print "Could not get machine name"
    LOCAL_MACHINE=os.popen("uname -n").readlines()
    print LOCAL_MACHINE
    sys.exit(-1)

if DATAFOLDER=="__unset__":
    raise RuntimeError("Didnt set DATAFOLDER properly.")


# MCC8.2 samples
# --------------

# MCC8.2 nue+cosmics: Tufts
#LARCV_SOURCE="/cluster/kappa/90-days-archive/wongjiradlab/larbys/data/mcc8.2/nue_cosmics/supera"
#LARLITE_SOURCE="/cluster/kappa/90-days-archive/wongjiradlab/larbys/data/mcc8.2/nue_cosmics/larlite"

# MCC8.2 nue+cosmics: Tufts
#LARCV_SOURCE="/cluster/kappa/90-days-archive/wongjiradlab/larbys/data/mcc8.2/numu_cosmics/supera"
#LARLITE_SOURCE="/cluster/kappa/90-days-archive/wongjiradlab/larbys/data/mcc8.2/numu_cosmics/larlite"

# MCC8.x Comparison Samples
# -------------------------

# 1e1p Nue+cosmics
#LARCV_SOURCE   = DATAFOLDER+"/comparison_samples/1e1p/supera_links"
#LARLITE_SOURCE = DATAFOLDER+"/comparison_samples/1e1p/larlite_links"

# 1mu1p Numu+cosmics
#LARCV_SOURCE   = DATAFOLDER+"/comparison_samples/1e1p/supera"
#LARLITE_SOURCE = DATAFOLDER+"/comparison_samples/1e1p/larlite"

# numu inclusive+cosmics
#LARCV_SOURCE   = DATAFOLDER+"/comparison_samples/inclusive_muon/supera_links"
#LARLITE_SOURCE = DATAFOLDER+"/comparison_samples/inclusive_muon/larlite_links"

# ncpizero
#LARCV_SOURCE   = DATAFOLDER+"/comparison_samples/ncpizero/supera_links"
#LARLITE_SOURCE = DATAFOLDER+"/comparison_samples/ncpizero/larlite_links"

# extbnb
LARCV_SOURCE   = DATAFOLDER+"/comparison_samples/extbnb_wprecuts/supera"
LARLITE_SOURCE = DATAFOLDER+"/comparison_samples/extbnb_wprecuts/larlite"

# corsika
#LARCV_SOURCE   = DATAFOLDER+"/comparison_samples/corsika/supera_wpmtprecut"
#LARLITE_SOURCE = DATAFOLDER+"/comparison_samples/corsika/larlite_wpmtprecut"

# BNB data, 5e19
#LARCV_SOURCE   = DATAFOLDER+"/bnbdata_5e19/supera"
#LARLITE_SOURCE = DATAFOLDER+"/bnbdata_5e19/larlite"


# We parse folder contents for larcv and larlite files
# We keep them in a dictionary
job_dict = {} # key=jobid, value=dict{"larlite":[],"larcv":[]}

files = os.listdir(LARCV_SOURCE)
for f in files:
    f = f.strip()
    if ".root" not in f or "larcv" not in f:
        continue
    fpath = LARCV_SOURCE + "/" + f
    fileid = int(f.split(".")[-2].split("_")[-1])
    #print f.strip(),fileid
    if fileid not in job_dict:
        job_dict[fileid] = {"larcv":[],"larlite":[]}
    job_dict[fileid]["larcv"].append(fpath)

files = os.listdir(LARLITE_SOURCE)
for f in files:
    f = f.strip()
    if ".root" not in f or "larlite" not in f:
        continue
    fpath = LARLITE_SOURCE + "/" + f
    fileid = int(f.split(".")[-2].split("_")[-1])
    #print f.strip(),fileid
    if fileid not in job_dict:
        job_dict[fileid] = {"larcv":[],"larlite":[]}
    job_dict[fileid]["larlite"].append(fpath)

fileid_list = job_dict.keys()
fileid_list.sort()

jobidlist = open("jobidlist.txt",'w')
os.system("mkdir -p inputlists")
os.system("rm -f inputlists/*")
for jobid,fileid in enumerate(fileid_list):
    flarcv = open("inputlists/input_larcv_%04d.txt"%(fileid),'w')
    for f in job_dict[fileid]["larcv"]:
        print >> flarcv,f
    flarcv.close()

    flarlite = open("inputlists/input_larlite_%04d.txt"%(fileid),'w')
    for f in job_dict[fileid]["larlite"]:
        if "simch" in f or "hist" in f or "wire" in f or "reco2d" in f:
            continue
        print >> flarlite,f
    flarlite.close()
    
    print >> jobidlist,fileid

jobidlist.close()


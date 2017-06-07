import os,sys

# SPECIFY FOLDER WHERE INPUT DATA LIVES
#LARCV_SOURCE="/cluster/tufts/wongjiradlab/larbys/data/mcc8/calmod_mcc8_bnb_nu_cosmic_v06_26_01_run01.09000_run01.09399_v01_p00_out"
#LARLITE_SOURCE="/cluster/tufts/wongjiradlab/larbys/data/mcc8/calmod_mcc8_bnb_nu_cosmic_v06_26_01_run01.09000_run01.09399_v01_p00_out"
LARCV_SOURCE="/cluster/kappa/90-days-archive//wongjiradlab/larbys/data/mcc8/calmod_mcc8_bnb_nu_cosmic_v06_26_01_run01.09000_run01.09399_v01_p00_out"
LARLITE_SOURCE="/cluster/kappa/90-days-archive/wongjiradlab/larbys/data/mcc8/calmod_mcc8_bnb_nu_cosmic_v06_26_01_run01.09000_run01.09399_v01_p00_out"

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
for jobid,fileid in enumerate(fileid_list):
    flarcv = open("inputlists/input_larcv_%03d.txt"%(fileid),'w')
    for f in job_dict[fileid]["larcv"]:
        print >> flarcv,f
    flarcv.close()

    flarlite = open("inputlists/input_larlite_%03d.txt"%(fileid),'w')
    for f in job_dict[fileid]["larlite"]:
        print >> flarlite,f
    flarlite.close()
    
    print >> jobidlist,jobid

jobidlist.close()

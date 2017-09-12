import os,sys
import ROOT as rt
from larcv import larcv

# files are not sorted or labeled ...
# we have to open EACH DAMN file and find first run,subrun,entry to pair them

# DATA
# ---------------

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

# 1e1p
#superafolder  = DATAFOLDER+"/comparison_samples/1e1p/supera"
#larlitefolder = DATAFOLDER+"/comparison_samples/1e1p/larlite"

# 1mu1p
superafolder  = DATAFOLDER+"/comparison_samples/1mu1p/supera"
larlitefolder = DATAFOLDER+"/comparison_samples/1mu1p/larlite"

fdict = {} # key: first (run,subrun,event), value: dict of file types

# SUPERA
superafiles = os.listdir( superafolder )
for f in superafiles:
    if ".root" not in f:
        continue

    try:
        rfile = rt.TFile(superafolder+"/"+f.strip())
        ttree = rfile.Get("partroi_segment_tree")
        ttree.GetEntry(0)
        img_br_name = "partroi_segment_branch"
        img_br=None
        exec('img_br=ttree.%s' % img_br_name)
        rse = (int(img_br.run()), int(img_br.subrun()), int(img_br.event()))
        
        if rse not in fdict:
            fdict[rse] = {}
        
        fdict[rse]["larcv"] = superafolder+"/"+f.strip()
        rfile.Close()
    except:
        print "Error with ",superafolder+"/"+f.strip()
        continue


# LARLITE
larlitefiles = os.listdir( larlitefolder )
for f in larlitefiles:
    if ".root" not in f:
        continue
    ftype = f.split("_")[1]

    try:
        rfile = rt.TFile(larlitefolder+"/"+f.strip())
        ttree = rfile.Get("larlite_id_tree")
        ttree.GetEntry(0)
        rse = (int(ttree._run_id), int(ttree._subrun_id), int(ttree._event_id))

        if rse not in fdict:
            fdict[rse] = {}
        
        fdict[rse][ftype] = larlitefolder+"/"+f.strip()
        print "Adding ",ftype," for ",rse
    except:
        print "Something wrong with ",f.strip()
        continue

# Dump and Make joblist
fkeys = fdict.keys()
fkeys.sort()
os.system("rm inputlists/*")
os.system("mkdir -p inputlists")
joblist = open("jobidlist.txt",'w')
for fkey in fkeys:
    print fkey,"-----------------------------------------"
    jobid = fkey[1]*1000000+fkey[2]
    flarcv = open("inputlists/input_larcv_%04d.txt"%(jobid),'w')
    flarlite = open("inputlists/input_larlite_%04d.txt"%(jobid),'w')
    print >> joblist,jobid
    for i,j in fdict[fkey].items():
        print "  ",i,":",j
        if i in ["larcv"]:
            print >> flarcv,j
        elif i in ["opreco"]:
            print >> flarlite,j
    flarcv.close()
    flarlite.close()
joblist.close()
    



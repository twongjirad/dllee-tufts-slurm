import os,sys
import ROOT as rt

# Check job id list. Check output folder. Check that tagger output files have entries (and same number of entries)
# based on checks, will produce rerun list

# MCC8.1 nue+MC cosmics: mccaffrey
#TAGGER_FOLDER="/home/taritree/larbys/data/mcc8.1/nue_1eNpfiltered/out_week0626/tagger"

# MCC8.1 MC corsika cosmics: mccaffrey
TAGGER_FOLDER="/home/taritree/larbys/data/mcc8.1/corsika_mc/out_week0626/tagger"


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
for l in ljobid:
    jobid = int(l.strip())
    if jobid in good_list or jobid in rerun_list:
        continue
    else:
        rerun_list.append(jobid)
fjobid.close()


frerun = open("rerunlist.txt",'w')
for jobid in rerun_list:
    print >> frerun,jobid
frerun.close()

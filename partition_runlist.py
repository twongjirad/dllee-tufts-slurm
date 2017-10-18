import os,sys

MAX_NUM_JOBS=100

orig_rerun_file = open("rerunlist.txt",'r')
orig_rerun_jobs = orig_rerun_file.readlines()
orig_rerun_file.close()


njobs = len(orig_rerun_jobs)
npartitions = njobs/MAX_NUM_JOBS

if njobs%MAX_NUM_JOBS!=0:
   npartitions += 1

for p in range(npartitions):
    part_rerun_file = open("rerunlist_p%02d.txt"%(p),'w')
    for j in range(p*MAX_NUM_JOBS,(p+1)*MAX_NUM_JOBS):
       if j>=njobs:
          break
       job = orig_rerun_jobs[j]
       job = job.strip()	
       print >> part_rerun_file,job	
    part_rerun_file.close()	
    

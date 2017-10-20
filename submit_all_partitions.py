import os,sys

for p in range(0,10):
    cmd = "sbatch submit_p%02d.sh"%(p)
    print cmd
    os.system(cmd)

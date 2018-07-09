import os,sys

for p in range(0,10):
    submitscript = "submit_p%02d.sh"%(p)
    if not os.path.exists(submitscript):
        continue

    cmd = "sbatch "+submitscript
    print cmd
    os.system(cmd)

import os,sys
os.environ["PUB_LOGGER_LEVEL"]="kLOGGER_WARNING"
import argparse

print "---------------------------"
print "Make inputlist from PUBS DB"
print "---------------------------"

parser = argparse.ArgumentParser( description="make input lists for projects.\n  returns \"RUN SUBRUN EVENT FILE1 FILE2 ...\" provided some criteria" )
parser.add_argument( "runtable", type=str, 
                     help="runtable from which the projects derive, e.g. 'mcc8v6_extbnb'. see http://nudot.lns.mit.edu/taritree/dlleepubsummary.html for list." )
parser.add_argument( "project",  type=str, help="project name for which we check status to make our selection, e.g. 'tagger','ssnet','vertex'" )
parser.add_argument( "status",   type=int, help="status of project. typical values: {0:unprocessed, 4:OK, 10:error}. (exception 'xferinput' where OK=3)" )
parser.add_argument( "-n", "--num", default=-1, type=int, help="number to process" )

args = parser.parse_args( sys.argv[1:] )

# clear current input lists
# -------------------------
print "destroying current input lists (in ./inputlists). OK? [y or Y]"

check = raw_input()

if check!="y" and check!="Y":
    print "Stopping."
    sys.exit(-1)


os.system("rm inputlists/*")


# get list of files from pubs
cmd = "dump_project_rse_and_files.py {} {} {} -f supera opreco".format( args.runtable, args.project, args.status )
print cmd

plist = os.popen( cmd )
llist = plist.readlines()

jlist = open("jobidlist.txt",'w')

print "PUBs returned %d entries"%(len(llist))

for n,l in enumerate(llist):

    if args.num>=0 and n>=args.num:
        break
    
    l = l.strip()
    info = l.split()
    run = int(info[0])
    subrun = int(info[1])
    supera = info[2]
    opreco = info[3]

    jobid = run*10000 + subrun

    inlist_larcv = open("inputlists/input_larcv_%010d.txt"%(jobid),'w')
    print >> inlist_larcv,supera
    inlist_larcv.close()

    inlist_larlite = open("inputlists/input_larlite_%010d.txt"%(jobid),'w')
    print >> inlist_larlite,supera
    inlist_larlite.close()
    
    print >> jlist,jobid


jlist.close()

print "Also prepare the rerunlist.txt? [y or Y] for yes"

check = raw_input()

if check=="y" or check=="Y":
    os.system("cp jobidlist.txt rerunlist.txt")

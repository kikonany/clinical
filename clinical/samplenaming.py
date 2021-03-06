#!/usr/bin/python
#
import sys
import datetime
import time
import glob
import re
import socket
import os
import select
from dbaccess import *
import subprocess
import psutil

textfile = sys.argv[1]

if (len(sys.argv)>2):
  configfile = sys.argv[2]
else:
  configfile = 'None'
pars = readconfig(configfile)

with create_tunnel(pars['TUNNELCMD']):

  with dbconnect(pars['CLINICALDBHOST'], pars['CLINICALDBPORT'], pars['STATSDB'], 
                        pars['CLINICALDBUSER'], pars['CLINICALDBPASSWD']) as dbc:

    ver = dbc.versioncheck(pars['STATSDB'], pars['DBVERSION'])

    if not ver == 'True':
      print "Wrong db " + ver
      exit(0) 

    with open(textfile, "r") as namfile:
      for line in namfile:
        names = {}
        name = line.rstrip().split("\t")
        if len(name) > 1:
          names['customerid'] = name[1]
          names['limsid'] = name[0]
        
        query = " SELECT sample_id, samplename, barcode FROM sample WHERE samplename LIKE '"+name[0]+"\_%' AND limsid is NULL "
        print query
        reply = dbc.generalquery(query)
        if len(reply) == 1:
          for rep in reply:
#            print rep['samplename'], name[0], name[1], str(names) #str(rep)
            dbc.insertorupdate( 'sample', 'samplename', rep['samplename'], names )
        else:
          print "NOT FOUND: ", str(names) 
 
      
    nas = socket.gethostname()
#    nasdir = pars['RUNFOLDER']
#    rundate = list(runfolder.split("_")[0])
#    rundate = "20"+rundate[0]+rundate[1]+"-"+rundate[2]+rundate[3]+"-"+rundate[4]+rundate[5]

#    nasdict = {'starttonas': starttonas, 'endtonas': endtonas, 'nas': nas, 'nasdir': nasdir, 
#           'runname': runfolder, 'startdate': rundate}

#    res = dbc.insertorupdate( "backup", "runname", runfolder, nasdict )
    print nas


exit(0)

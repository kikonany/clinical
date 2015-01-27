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
    else:
      print "Correct db"
      
    for root, dirs, files in os.walk(pars['CLUSTERBACKUP']):
      for file in files:
        if file.endswith(".tar.gz"):
          runname = file[:-7]
          print runname
          if (os.path.isfile(pars['CLUSTERBACKUP'] + file) and 
              os.path.isfile(pars['CLUSTERBACKUP'] + file + ".md5.txt")):
            inbackupdir = str(1)
          else:
            sys.exit("not "+pars['CLUSTERBACKUP'] + file + " or "+pars['CLUSTERBACKUP'] + file + ".md5.txt")

          rundate = list(runname.split("_")[0])
          rundate = "20"+rundate[0]+rundate[1]+"-"+rundate[2]+rundate[3]+"-"+rundate[4]+rundate[5]
          clusterdict = {'inbackupdir': inbackupdir, 'runname': runname, 'startdate': rundate}
#          res = dbc.insertorupdate( "backup", "runname", runname, nasdict )
          print clusterdict
    for root, dirs, fils in os.walk(pars['ONTAPEFOLDER']):
      for tapedir in dirs:
        print tapedir
        for rot, drs, files in os.walk(pars['ONTAPEFOLDER'] + tapedir):
          textcontent = ""
          for file in files:
            if file.endswith(".txt"):
              textcontent += file.read()
          print textcontent
          for file in files:
            if file.endswith(".tar.gz"):
              if (os.path.isfile(pars['ONTAPEFOLDER'] + tapedir + "/" + file) and 
                  os.path.isfile(pars['ONTAPEFOLDER'] + tapedir + "/" + file + ".md5.txt")):
                tapeentry = dbc.getprimarykey( 'backuptape', 'tapedir', tapedir )
                if tapeentry['backuptape_id'] == 0:
                  print tapedir, runname, str(tapeentry)
                  

              runname = file[:-7]
              print runname
              rundate = list(runname.split("_")[0])
              rundate = "20"+rundate[0]+rundate[1]+"-"+rundate[2]+rundate[3]+"-"+rundate[4]+rundate[5]
              tapedict = {'inbackupdir': inbackupdir, 'runname': runname, 'startdate': rundate}
              tapedict = dict(tapeentry.items() + tapedict.items())
              print tapedict
          

exit(0)

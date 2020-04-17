#!/usr/bin/python
### Python script to use SNAP as InSAR processor compatible with StaMPS PSI processing
# Author Jose Manuel Delgado Blasco
# Date: 21/06/2018
# Version: 1.0
# Step 1 : preparing slaves in folder structure
# Step 2 : TOPSAR Splitting (Assembling) and Apply Orbit
# Step 3 : Coregistration and Interferogram generation
# Step 4 : StaMPS export
# Added option for CACHE and CPU specification by user
# Planned support for DEM selection and ORBIT type selection 


# case 1: 1 swath in one slice 
# case 2: 2 swath in one slice -> apply slice assembly 
# case 3: 1 swath in two slice -> need merge

import os
from pathlib import Path
import sys
import glob
import subprocess
import shlex
import time
import zipfile
from IWs import getBurst
inputfile = sys.argv[1]
# inputfile="proj.conf"
bar_message='\n#####################################################################\n'

# Getting configuration variables from inputfile
try:
    in_file = open(inputfile, 'r')
    for line in in_file.readlines():
        if "PROJECTFOLDER" in line:
            PROJECT = line.split('=')[1].strip()
            print PROJECT
        if "IWs" in line:
            IW = line.split('=')[1].strip()
            print IW
        if "GRAPHSFOLDER" in line:
            GRAPH = line.split('=')[1].strip()
            print GRAPH
        if "GPTBIN_PATH" in line:
            GPT = line.split('=')[1].strip()
            print GPT
        if "LONMIN" in line:
            LONMIN = line.split('=')[1].strip()
        if "LATMIN" in line:
            LATMIN = line.split('=')[1].strip()
        if "LONMAX" in line:
            LONMAX = line.split('=')[1].strip()
        if "LATMAX" in line:
            LATMAX = line.split('=')[1].strip()
        if "CACHE" in line:
            CACHE = line.split('=')[1].strip()
        if "CPU" in line:
            CPU = line.split('=')[1].strip()
finally:
        in_file.close()

#############################################################################
### TOPSAR Splitting (Assembling) and Apply Orbit section ####
############################################################################
slavefolder=PROJECT+'/slaves'
splitfolder=PROJECT+'/split'
logfolder=PROJECT+'/logs'
graphfolder=PROJECT+'/graphs'
if not os.path.exists(splitfolder):
                os.makedirs(splitfolder)
if not os.path.exists(logfolder):
                os.makedirs(logfolder)
if not os.path.exists(graphfolder):
                os.makedirs(graphfolder)

polygon=[[float(LONMIN),float(LATMIN)],[float(LONMIN),float(LATMAX)],[float(LONMAX),float(LATMAX)],[float(LONMAX),float(LATMIN)]]


graph2run=PROJECT+'/graphs/splitgraph2run.xml'
outlog=logfolder+'/split_proc_stdout.log'
out_file = open(outlog, 'a')
err_file=out_file

print bar_message
out_file.write(bar_message)
message='## TOPSAR Splitting and Apply Orbit\n'
print message
out_file.write(message)
print bar_message
out_file.write(bar_message)



k=0

    
for acdatefolder in sorted(os.listdir(slavefolder)):
    k=k+1
    print '['+str(k)+'] Folder: '+acdatefolder
    out_file.write('['+str(k)+'] Folder: '+acdatefolder+'\n')
    print os.path.join(slavefolder, acdatefolder)
    out_file.write(str(os.path.join(slavefolder, acdatefolder))+'\n')
    files = glob.glob(os.path.join(slavefolder, acdatefolder) + '/*.zip')
    print files
    out_file.write(str(files)+'\n')
    head, tail = os.path.split(os.path.join(str(files)))
    splitslavefolder=splitfolder+'/'+tail[17:25]
    if not os.path.exists(splitslavefolder):
                os.makedirs(splitslavefolder)

    # need new nameing method
    

    # slave_split_applyorbit
    '''
    Read -> TOPSAR-Split -> Apply-Orbit-File -> Write
            IWs/VV/1-9999
    '''
    if len(files) == 1:
    	graphxml=GRAPH+'/slave_split_applyorbit_readIWs.xml'
        # Read in the file
        print 'FILE(s) : '+files[0]
        
        gb=getBurst(polygon,files[0])
        for swi in gb:
        	if gb[swi]==[-1,-1]:
        	  	continue
        	IWi=swi[88:91].upper()
        	outputname=tail[17:25]+'_'+IWi+'.dim'
        	with open(graphxml, 'r') as file :
        		filedata = file.read()
        	# Replace the target string
        	filedata = filedata.replace('INPUTFILE', files[0])
        	filedata = filedata.replace('IWs',IWi)
        	filedata = filedata.replace('OUTPUTFILE',splitslavefolder+'/'+outputname)
        	filedata = filedata.replace('BST0',str(gb[swi][0]))
        	filedata = filedata.replace('BST1',str(gb[swi][1]))
        	# Write the file out again
        	with open(graph2run, 'w') as file:
        		file.write(filedata)
        	# run proecess
        	args = [ GPT, graph2run, '-c', CACHE, '-q', CPU]
        	print args
        	out_file.write(str(args)+'\n')
        	# launching the process
        	process = subprocess.Popen(args, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        	timeStarted = time.time()
        	stdout = process.communicate()[0]
        	print 'SNAP STDOUT:{}'.format(stdout)
        	timeDelta = time.time() - timeStarted                     # Get execution time.
        	print('['+str(k)+'] Finished process in '+str(timeDelta)+' seconds.')
        	out_file.write('['+str(k)+'] Finished process in '+str(timeDelta)+' seconds.\n')
        	if process.returncode != 0 :
        		message='Error splitting slave '+str(files)
        		err_file.write(message)
        	else: 
        		message='Split slave '+str(files)+' successfully completed.\n'
        	print message
        	out_file.write(message)
        	print bar_message
        	out_file.write(bar_message)

    # graph: slaves_assamble_split_applyorits
    # use more than two "slice" for one swath (testing)
    if len(files) > 1 :
    	graphxml=GRAPH+'/slaves_assemble_split_applyorbit.xml'
        with open(graphxml, 'r') as file :
           filedata = file.read()
        # Replace the target string
        filedata = filedata.replace('INPUTFILE1', files[0])

    	filedata = filedata.replace('INPUTFILE2', files[1])
    	filedata = filedata.replace('IWs',IW)
        # filedata=filedata.replace("IWs",IW)
        filedata = filedata.replace('OUTPUTFILE',splitslavefolder+'/'+outputname)
        with open(graph2run, 'w') as file:
            file.write(filedata)



 #    # run proecess
 #    args = [ GPT, graph2run, '-c', CACHE, '-q', CPU]
 #    print args
 #    out_file.write(str(args)+'\n')
 #    # launching the process
 #    process = subprocess.Popen(args, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 #    timeStarted = time.time()
 #    stdout = process.communicate()[0]
 #    print 'SNAP STDOUT:{}'.format(stdout)
 #    timeDelta = time.time() - timeStarted                     # Get execution time.
 #    print('['+str(k)+'] Finished process in '+str(timeDelta)+' seconds.')
 #    out_file.write('['+str(k)+'] Finished process in '+str(timeDelta)+' seconds.\n')
 #    if process.returncode != 0 :
	# message='Error splitting slave '+str(files)
	# err_file.write(message)
 #    else: 
	# message='Split slave '+str(files)+' successfully completed.\n'
	# print message
	# out_file.write(message)
 #    print bar_message
 #    out_file.write(bar_message)
out_file.close()

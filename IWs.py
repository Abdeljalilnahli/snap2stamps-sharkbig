#!/usr/bin/python
from __future__ import print_function
import numpy as np
import zipfile, glob, os
from inSide import inSide
from sys import argv


inputfile="project.conf"
#argv[1]
fp=open(inputfile)
for line in fp.readlines():
	if "PROJECTFOLDER" in line:
		PROJECT = line.split('=')[1].strip()
	if "LONMIN" in line:
		LONMIN = line.split('=')[1].strip()
	if "LATMIN" in line:
		LATMIN = line.split('=')[1].strip()
	if "LONMAX" in line:
		LONMAX = line.split('=')[1].strip()
	if "LATMAX" in line:
		LATMAX = line.split('=')[1].strip()


# check if log directory exits.
logfolder=PROJECT+'/logs'
# if not os.path.exists(logfolder):
#                 os.makedirs(logfolder)
log=open(logfolder+"/swath_list",'w')



nr=11
nc=21
# polygon='POLYGON (('+LONMIN+' '+LATMIN+','+LONMAX+' '+LATMIN+','+LONMAX+' '+LATMAX+','+LONMIN+' '+LATMAX+','+LONMIN+' '+LATMIN+'))'
polygon=[[float(LONMIN),float(LATMIN)],[float(LONMIN),float(LATMAX)],[float(LONMAX),float(LATMAX)],[float(LONMAX),float(LATMIN)]]

zips=sorted(glob.glob("slaves/*/*.zip"))

for slave in zips:
	print(slave,end="\t")
	log.write(slave+"\t")
	try:
		lsname=zipfile.ZipFile(slave).namelist()	
	except:
		print('iw1\t-1\t-1\tiw2\t-1\t-1\tiw3\t-1\t-1')
		log.write('\tiw1\t-1\t-1\tiw2\t-1\t-1\tiw3\t-1\t-1\n')
		continue
	vv= []
	for i in lsname:
		seg=i.split('/')
		if "annotation" == seg[1]: 
			if "vv" in seg[2]:
				vv.append(i)
	vv=sorted(vv)
	# print(slave,vv[0])
	for iw in range(len(vv)):
		SWs=zipfile.ZipFile(slave).open(vv[iw],'r')
		count=0
		line=True
		tag=False
		lats=[]
		lons=[]
		while line:
			line=SWs.readline().strip()
			if b"<geolocationGridPoint>" == line:
				tag=True
			elif (b"</geolocationGridPoint>" == line):
				tag=False
				continue

			if b"<latitude>" in line and  tag:
				lat=float(line.split(b'</')[0].split(b">")[1])
				lats.append(lat)
			elif b"<longitude>" in line and tag:
				lon=float(line.split(b'</')[0].split(b">")[1])
				lons.append(lon)
				count+=1
		# symbols for ascending but for descending works
		
		maxbst=-2
		minbst=12
		for i in zip(lons,lats):
			if inSide(polygon,[i[0],i[1]]):
				bst=lats.index(i[1])//21
				if bst>=maxbst:
					maxbst=bst
				if bst<=minbst:
					minbst=bst

		if minbst==12: minbst=-1
		print(vv[iw][88:91]+  "\t" + "%i\t%i"%(minbst,maxbst+1), end="\t")
		log.write(vv[iw][88:91]+ "\t" + "%i\t%i"%(minbst,maxbst+1)+"\t")
		# plt.plot(lons,lats,'o',ms=1)
		SWs.close()
	print()
	log.write("\n")



#!/usr/bin/python
# the function getButst is only for one slice.

from __future__ import print_function
import numpy as np
import zipfile, glob, os
from inSide import inSide
from sys import argv

inputfile=argv[1]
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
slavefolder=PROJECT+'/slaves'

if not os.path.exists(logfolder):
                os.makedirs(logfolder)
log=open(logfolder+"/IW_list",'w')



nr=11
nc=21
# polygon='POLYGON (('+LONMIN+' '+LATMIN+','+LONMAX+' '+LATMIN+','+LONMAX+' '+LATMAX+','+LONMIN+' '+LATMAX+','+LONMIN+' '+LATMIN+'))'
polygon=[[float(LONMIN),float(LATMIN)],[float(LONMIN),float(LATMAX)],[float(LONMAX),float(LATMAX)],[float(LONMAX),float(LATMIN)]]

def getBurst(poly,fzip):
	_bst=[]

	try:
		lsname=zipfile.ZipFile(fzip).namelist()	 # open zipfile
	except:
		_bst=[[-1,-1],[-1,-1],[-1,-1]]
	vv= []
	for i in lsname:
		seg=i.split('/')
		if "annotation" == seg[1]: 
			if "vv" in seg[2]:
				vv.append(i)
	vv=sorted(vv)
	for iw in range(len(vv)):
		SWs=zipfile.ZipFile(fzip).open(vv[iw],'r')
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
		maxbst=-1
		minbst=12
		for i in zip(lons,lats):
			if inSide(poly,[i[0],i[1]]):
				bst=lats.index(i[1])//21
				if bst>=maxbst:
					maxbst=bst+1
				if bst<=minbst:
					minbst=bst
		if maxbst==11: maxbst=10
		if minbst==0 : minbst=1
		if minbst==12: minbst=-1 

		# print(slave," ",vv[iw][88:91].upper()+  " %i %i"%(minbst,maxbst+1))
		_bst.append([minbst,maxbst])
		SWs.close()
		
	return dict(zip(vv,_bst))



if __name__ == "__main__":
	zips=sorted(glob.glob(slavefolder+"/*/*.zip"))
	for slave in zips:
		ans=getBurst(polygon,slave)
		for _vv in ans:
			print(slave,_vv[88:91].upper(), ans[_vv][0], ans[_vv][1], file=log)
			print(slave,_vv[88:91].upper(), ans[_vv][0], ans[_vv][1])

log.close()

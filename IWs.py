import numpy as np
import zipfile,glob
from inSide import inSide

for iw in range(len(vv)):
	SWs=open(vv[iw],'r')
	count=0
	line=True
	tag=False
	lats=[]
	lons=[]
	while line:
		line=SWs.readline().strip()
		if "<geolocationGridPoint>" == line:
			tag=True
		elif ("</geolocationGridPoint>" == line):
			tag=False
			continue

		if "<latitude>" in line and  tag:
			lat=float(line.split('</')[0].split(">")[1])
			lats.append(lat)
		elif "<longitude>" in line and tag:
			lon=float(line.split('</')[0].split(">")[1])
			lons.append(lon)
			# plt.plot(lon,lat,color[i]+'o', ms=1)
			count+=1
	# symbols for ascending but for descending works
	nr=11
	nc=21
	
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
	print('IW'+str(iw+1),end='')
	print(",%i, %i"%(minbst,maxbst+1),end=',')


	plt.plot(lons,lats,'o', ms=2)
	SWs.close()
print()
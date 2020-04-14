import numpy as np
import glob

file='s1a-iw{}-slc-vv-20191231t100110-20191231t100138-030591-038128-00{}.xml'
vv=glob.glob("*iw[1-3]-slc-vv*")


lon0=119.485,122.3312
lat0=24.118,25.3943 
polygon=[[lon0[0],lat0[0]],[lon0[1],lat0[0]],[ lon0[1], lat0[1] ], [lon0[0],lat0[1]]]




margin=[]
for i in range(len(vv)):
	SWs=open(vv[i],'r')
	count=0
	line=True
	color=['r','g','b']
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

		# Tag switch is added.
		if "<latitude>" in line and  tag:
			lat=float(line.split('</')[0].split(">")[1])
			lats.append(lat)
		elif "<longitude>" in line and tag:
			lon=float(line.split('</')[0].split(">")[1])
			lons.append(lon)
			plt.plot(lon,lat,color[i]+'o', ms=1)
			count+=1
	# symbols for ascending but for descending works
	left=max(lons),lats[lons.index(max(lons))]
	right=min(lons),lats[lons.index(min(lons))]
	up=lons[lats.index(max(lats))],max(lats)
	down=lons[lats.index(min(lats))],min(lats)
	swath=[left,up,right,down]
	print('IW',i+1,end=' ')
	print(ifUnion(polygon,swath))

	SWs.close()

for i in polygon:
		plt.plot(i[0],i[1],'ro')
plt.show()


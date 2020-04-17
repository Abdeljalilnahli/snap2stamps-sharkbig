# algorithm: test if all the point is in the swath.
# reference: https://www.geeksforgeeks.org/how-to-check-if-a-given-point-lies-inside-a-polygon/
# struct Point { int x; int y;};
# examine if q is on line pr

def onSegment(p,q,r):
	if q[0]<=max(p[0],r[0]) and q[0]>=min(p[0],r[0]) and q[1]<=max(p[1],r[1]) and q[1]>=min(p[1],r[1]):
	   return True 
	else:
		return False

# The orientation of three point:
# 0: colinear
# 1: clockwise
# 2: counterclockwise


def orientation(p,q,r):
	# cross priduct of vector pq and pr
	val=(q[1]-p[1])*(r[0]-q[0])- (q[0] - p[0])*(r[1] - q[1])
	if val == 0:
		return 0
	elif val>0:
		return 1
	else: 
		return 2

def doIntersect(p1,q1,p2,q2):
	o1=orientation(p1,q1,p2)
	o2=orientation(p1,q1,q2)
	o3=orientation(p2,q2,p1)
	o4=orientation(p2,q2,q1)

	if (o1!=o2) and (o3!=o4):
		return True
	if o1 == 0 and onSegment(p1,p2,q1):
		return True
	if o2 ==0 and onSegment(p1,q2,q1):
		return True
	if o3 ==0 and onSegment(p2,p1,q2):
		return True
	if o4==0 and onSegment(p2,q1,q2):
		return True

	return False

# polygon=[[x1,y1],[x2,y2],[x3,y3]]
def inSide(polygon,p):

	n=len(polygon)
	if n<3:
		return False
	ext=[1e23,p[1]]
	count=0
	for i in range(n):
		nx=(i+1)%n
		if doIntersect(polygon[i],polygon[nx],p,ext):
			if (orientation(polygon[i],p,polygon[nx]) == 0 ):
				# Return True if point on the edge.
				return onSegment(polygon[i],p,polygon[nx])
				# return none
			
			count+=1

	if count%2==0:
		return  False
	else:
		return True
def onEdge(polygon,p):
	n=len(polygon)
	for i in range(n):
		ni=(i+1)%n

		if orientation(polygon[i],p,polygon[ni])==0 and \
		onSegment(polygon[i], p, polygon[ni])==True:
			return True
	return False




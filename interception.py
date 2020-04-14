from osgeo import ogr

def isInterception(poly1,poly2):
	poly1=ogr.Geometry(ogr.wkbLinearRing)
	poly2=ogr.Geometry(ogr.wkbLinearRing)
	for i in polygon1:
		poly1.AddPoint(i[0],i[1])
	poly1.AddPoint(polygon1[0][0],polygon1[0][1])
	geom1=ogr.Geometry(ogr.wkbPolygon)
	geom1.AddGeometry(poly1)
	for i in polygon2:
		poly2.AddPoint(i[0],i[1])
	poly2.AddPoint(polygon2[0][0],polygon2[0][1])
	geom2=ogr.Geometry(ogr.wkbPolygon)
	geom2.AddGeometry(poly2)

	inter = geom1.Intersection(geom2)
	area=inter.GetArea()
	if area>0:
		return True
	else:
		return False


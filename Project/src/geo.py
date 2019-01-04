from math import sin, cos, sqrt, atan2, radians

def distance(l1: dict,l2: dict):
	R = 6373000 #m
	loc1 = dict()
	loc2 = dict()			
	loc1["lat"] = radians(l1["lat"])
	loc1["lon"] = radians(l1["lon"])


	loc2["lat"] = radians(l2["lat"])
	loc2["lon"] = radians(l2["lon"])

	dlon = loc2["lon"] - loc1["lon"]
	dlat = loc2["lat"] - loc1["lat"]

	a = sin(dlat / 2)**2 + cos(loc1["lat"]) * cos(loc2["lat"]) * sin(dlon / 2)**2
	c = 2 * atan2(sqrt(a), sqrt(1 - a))
	distance = R * c
	return distance

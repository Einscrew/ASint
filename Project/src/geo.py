from math import sin, cos, sqrt, atan2, radians


def distance(l1: dict,l2: dict):
	R = 6373000 #m
	l1["lat"] = radians(l1["lat"])
	l1["lon"] = radians(l1["lon"])


	l2["lat"] = radians(l2["lat"])
	l2["lon"] = radians(l2["lon"])
	
	dlon = l2["lon"] - l1["lon"]
	dlat = l2["lat"] - l1["lat"]

	a = sin(dlat / 2)**2 + cos(l1["lat"]) * cos(l2["lat"]) * sin(dlon / 2)**2
	c = 2 * atan2(sqrt(a), sqrt(1 - a))
	distance = R * c
	return distance

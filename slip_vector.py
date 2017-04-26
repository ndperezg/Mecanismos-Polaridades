import numpy as np
import sys, os

def slip_vector(strike,dip,rake):
	x = (np.cos(rake)*np.cos(strike)) + (np.sin(rake)*np.cos(dip)*np.cos(strike))
	y = (np.sin(rake)*np.cos(dip)*np.cos(strike)) - (np.cos(rake)*np.sin(strike))
	z = np.sin(rake)*np.sin(dip)
	return [x, y, z]





if len(sys.argv)<2:
	print "No hay parametros suficientes"
	sys.exit()

arc = open(sys.argv[1])

for line in arc:
	planes = line.split()
	date = planes[0]
	stk1, dip1, rk1, stk2, dip2, rk2 = float(planes[6]), float(planes[7]), float(planes[8]), float(planes[9]), float(planes[10]), float(planes[11])
	vector1 = slip_vector(stk1,dip1,rk1)
	vector2 = slip_vector(stk2, dip2, rk2)
	print "%s %s %s"%(date,vector1,vector2)

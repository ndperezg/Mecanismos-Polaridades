import numpy as np
import os, sys

def RA(Mw):
	"""
	Rupture area (km2)
	"""
	logRA = (0.91*Mw) - 3.49
	return 10**logRA

def RLD(Mw):
	"""
	Subsurface rupture lenght (km)
	"""
	logRLD = (0.59*Mw) - 2.44
	return 10**logRLD

def SLR(Mw):
	"""
	surface rupture lenght (km)
	"""
	logSLR = (1.49*Mw) + 4.38
	return 10**logSLR

def AD(Mw):
	"""
	average displacement
	"""
	logAD = (0.69*Mw) - 4.80
	return 10**logAD

def MD(Mw):
	"""
	maximum displacement (m)
	"""
	logMD = (0.82*Mw) - 5.46
	return 10**logMD

def MW(mu,D,A):
	logMo = np.log10(mu*D*A)
	Mw = ((logMo)/1.5) - 10.73
	return Mw



if len(sys.argv)<2:
	print "no hay parametros suficientes"
	sys.exit()

#print "Event 1 %s %s %s %s %s %s"%(4.0, RA(4.0), MD(4.0), AD(4.0), RLD(4.0), SLR(4.0))

arc = open(sys.argv[1])
mu = 5e11 # dyn/cm2

print "   Event     Mw       RA(km^2)        MD(m)                AD(m)           RLD(km)           SLR(km)          Mw_AD              Mw_MD                abs(Mw-M_AD)            abs(Mw_MD) "

for line in arc:
	f = line.split()
	Mw, name = float(f[1]), f[0]
	print "%s   %s   %s   %s   %s   %s   %s     %s       %s       %s       %s"%(name, Mw, RA(Mw), MD(Mw), AD(Mw), RLD(Mw), SLR(Mw), MW(mu, AD(Mw)*(1e2), RLD(Mw)*(1e10)), MW(mu, MD(Mw)*(1e2), RLD(Mw)*1e10), abs(Mw - MW(mu, AD(Mw)*(1e2), RLD(Mw)*(1e10))), abs(Mw - MW(mu, MD(Mw)*(1e2), RLD(Mw)*(1e10))))

arc.close()
		

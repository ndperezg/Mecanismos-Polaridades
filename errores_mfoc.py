from glob import glob
import os, sys
import numpy as np
import matplotlib.pyplot as plt

def figuras(lista, angle, l):
	fig = plt.figure()
	hist_gap=plt.hist(lista,bins=np.arange(0,360,2))
	plt.xlabel('error %s ($^\circ$)'%angle,fontsize=18)
	plt.ylabel('Numero de sismos',fontsize=18)
	plt.title('Total sismos: %s'%l)
	fig.savefig('%s.png'%angle)
	#plt.show()

directory = "best_sfile"
if not os.path.exists(directory):
	os.makedirs(directory)

log = open('sfiles.log','w+')

sfiles = glob('*L.S*')
err_strike, err_dip, err_rake = [], [], []
counter = 0

e = float(raw_input('Ingrese el error maximo en grados:\n'))

for s in sfiles:
	sfile = open(s)
	try:
		for line in sfile:
			if line[79] == 'F' and line[70:75] == 'FPFIT':
				split = line.strip().split()
				strike, dip, rake = float(split[3]), float(split[4]), float(split[5])
				if strike <= e:
					if dip <= e:
						if rake <= e:
							os.system("cp %s %s"%(s,directory))
							counter += 1
				err_strike.append(strike)
				err_dip.append(dip)
				err_rake.append(rake)
			else:
				pass
	except:
		print >> log, "Error en %s"%sfile.name

	sfile.close()

l = len(err_strike)
figuras(err_strike, 'Strike', l)
figuras(err_dip, 'Dip', l)
figuras(err_rake, 'Rake', l)
log.close()
print "Total sfiles con errores menores a %s grados: %s"%(e,counter)

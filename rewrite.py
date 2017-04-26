from glob import glob
import os, sys
def rewritesfile(sfile_velest, sfile_org, directory):
	new = directory+sfile_org.split('/')[1]
	#n = open(new,'w+')
	with open(sfile_velest) as infile:
		for line in infile:
			if line[79] == '1':
				l = list(line)
				l[43], l[44] = 'F', 'F'
				line1 = "".join(l)
			elif line[79] == 'E':
				lineE = line
			else:
				pass
	with open(new, 'w+') as n:
		with open(sfile_org) as outfile:
			for line in outfile:
				if line[79] == '1':
					line = line1
				elif line[79] == 'E':
					line = lineE
				if line[79] != 'F':
					n.write(line)

original = sorted(glob('errores_mfoc/*L.S*'))
velest = sorted(glob('split_velest/*L.S*'))

directory = '/home/nelson/Inducida/Mecanismos_Polaridades/renombrado/'

if not os.path.exists(directory):
	os.makedirs(directory)

for i in range(len(original)):
	rewritesfile(velest[i], original[i], directory)
	print original[i], velest[i]
	

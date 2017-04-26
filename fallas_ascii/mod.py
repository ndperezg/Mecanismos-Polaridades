import os, sys

old = open('fallas.bln')
new = open('fallas_mod.bln', 'w+')

counter = 0
for line in old:
	sep = line.split(',')
	if len(sep)>2:
		new.write('%s %s %s\n'%(sep[0], sep[1], counter))
	else:
		counter+=1
		new.write('%s\n'%(counter))


old.close()
new.close()

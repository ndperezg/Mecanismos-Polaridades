from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
from obspy.imaging.beachball import beach
from glob import glob
import os, sys

if len(sys.argv)<2:
	print "No hay parametros suficientes"
	sys.exit()

datos = open(sys.argv[1])

####Flags
arcgis = False
draw_rivers = False
draw_stations = True
draw_focmec = True
draw_lineamientos = False
draw_fallas = False
draw_fallas_ascii = True
###Leer y dibujar fallas en ascii
def fallas_ascii(arc,tipo):
	a = open(arc)
	d = dict()
	for line in a:
		if tipo == 1:
			sep = line.split()
		elif tipo == 2:
			sep = line.split(',')
		if len(sep)>1:
			key, lon, lat = sep[2].strip(), float(sep[0]), float(sep[1])
			if key in d:
				d[key][0].append(lon)
				d[key][1].append(lat)
			else:
				LON, LAT = [], []
				LON.append(lon)
				LAT.append(lat)
				d[key] = [LON, LAT]
	a.close()
	return d

def plot_fallas_ascii(d, map, color,ls):
		for key in d:
			print key
			x, y = map(d[key][0],d[key][1])
			map.plot(x,y, marker=None,color=color,lw=3.0,ls=ls)
			
###Color mecanismo focal
def beachcolor(rake):
	if -45 <= rake < 45:
		facecolor = 'r'
	elif 45 <= rake < 135:
		facecolor = 'k'
	elif 135 <= rake <= 180:
		facecolor = 'r'
	elif -180 <= rake < -135:
		facecolor = 'r'
	elif -135 <= rake < -45:
		facecolor = 'b'
	return facecolor


facecolor = 'b'




fig = plt.figure()
map = Basemap(llcrnrlon=-71.7,llcrnrlat=3.70,urcrnrlon=-71.3,urcrnrlat=4.00, projection='cyl')
map.drawparallels(np.linspace(3.5, 4.5, 20), labels=[1, 1, 0, 0], fmt="%.2f", dashes=[2, 2])
map.drawmeridians(np.linspace(-72., -71., 20), labels=[0, 0, 1, 1], fmt="%.2f", dashes=[2, 2])

###Mapa base de arcgis
if arcgis:
	map.arcgisimage(service='NatGeo_World_Map', xpixels = 1500, verbose= True)
else:
	pass


###Rios
if draw_rivers:
	map.readshapefile('/home/nelson/Inducida/Mecanismos_Polaridades/RIOS/COL_water_lines_dcw', 'COL_water_lines_dcw',linewidth=1.5,color='#40a4df')


###Dibuja estaciones:
if draw_stations:
	estaciones = open('camporubiales_stations.csv')
	names, sta_lats, sta_lons = [], [], []
	counter = 0
	for line in estaciones:
		if counter >= 1:
			names.append(line.split(',')[0])
			sta_lats.append(line.split(',')[7])
			sta_lons.append(line.split(',')[6])
		counter += 1
	x, y = map(sta_lons, sta_lats)
	map.scatter(x, y, 200, color="r", marker="^", edgecolor="k", zorder=3)
	for i in range(len(names)):
	    plt.text(x[i], y[i], names[i], va="top", family="monospace", weight="bold")
	estaciones.close()

###Dibuja mecanismos
if draw_focmec:
	focmec, lat, lon = [], [], []
	for line in datos:
		focmec.append([float(line.split()[3]),float(line.split()[4]),float(line.split()[5])])
		lat.append(float(line.split()[1]))
		lon.append(float(line.split()[0]))
	x, y = map(lon, lat)
	ax = plt.gca()
	for i in range(len(focmec)):
	    facecolor = beachcolor(focmec[i][2])
	    b = beach(focmec[i], xy=(x[i], y[i]), width=0.015, linewidth=1, facecolor=facecolor, alpha = 0.5)
	    b.set_zorder(10)
	    ax.add_collection(b)
	datos.close()


###Lineamientos:
if draw_lineamientos:
	lineamientos = open('lineamientospgaitan.csv')
	counter = 0
	for line in lineamientos:
		if counter>=1:
			linea = line.split(')')[0].split('(')[1]
			punto_1, punto_2 = linea.split(',')[0], linea.split(',')[1]
			linlats, linlons = [], []
			linlats.append(punto_1.split()[1])
			linlats.append(punto_2.split()[1])
			linlons.append(punto_1.split()[0]) 
			linlons.append(punto_2.split()[0])
			x, y = map(linlons,linlats)
			map.plot(x,y, marker=None,color='k',lw=3.0)
		counter +=1
	lineamientos.close()			

#map.scatter(x, y, 200, color="r", marker="v", edgecolor="k", zorder=3)

####Fallas
if draw_fallas:
	fallas = glob('CSV_wgs84/*.csv')
	for falla in fallas:
		print falla
		fault = open(falla)
		counter = 0
		lons, lats = [], []
		for line in fault:
			if counter >= 1:
				lon, lat = line.split(',')[0], line.split(',')[1]
				lons.append(lon)
				lats.append(lat)
			counter += 1
		x, y = map(lons, lats)
		map.plot(x,y, marker=None,color='b',lw=1.0)
	fault.close()
###Fallas ASCII:
if draw_fallas_ascii:
	d1 = fallas_ascii('fallas_ascii/fallas_mod.bln', 1)
	plot_fallas_ascii(d1,map,(0.5,0.5,0.5),'-')
	d2 = fallas_ascii('fallas_ascii/arenasbasales_carbonera-nodes.bln', 1)
	plot_fallas_ascii(d2,map,(0.2,0.6,0.45),'-')
	d3 = fallas_ascii('fallas_ascii/fallas_carbonera_rubiales.bln', 2)
	plot_fallas_ascii(d3,map,(0.2,0.6,0.45),'-')
	d4 = fallas_ascii('fallas_ascii/basamento_cristalino_posibles-nodes.bln', 1)
	plot_fallas_ascii(d4,map,(0.8,0.6,0.2),'--')
	d5 = fallas_ascii('fallas_ascii/basamento_cristalino-nodes.bln', 1)
	plot_fallas_ascii(d5,map,(0.8,0.6,0.2),'-')
	d6 = fallas_ascii('fallas_ascii/fallas_basamento_Rubiales.bln', 2)
	plot_fallas_ascii(d6,map,(0.8,0.6,0.2),'-')
"""
	#d1 = fallas_ascii('fallas_ascii/arenasbasales_carbonera-nodes.bln', 1)
	#print '========================'
	#d2 = fallas_ascii('fallas_ascii/fallas_carbonera_rubiales.bln', 2)
	#plot_fallas_ascii(d2,map,'b')

"""
#######################
#ax.set_title('Mecanismos focales con polaridades: %s eventos\n'%len(focmec), fontsize=25)
#map.drawmapscale(50, -75, 0, 0, 400)
plt.show()

#!/usr/bin/env python
import re
from glob import glob
from readCampbellGPS import readCampbellGPS

wkdir = '201802012132_akamalik_CR1000'
basedir = '/Users/dfc/Documents/ARC/RoyalGreenland/MET/'
datadir = basedir + wkdir + '/'
srch5 = '*_FiveMin.dat'
metfiles = glob(datadir+srch5)
srch1 = '*_OneSec.dat'
gpsfiles = glob(datadir+srch1)

allmetfn = basedir + wkdir + '_met.txt'
fout = open(allmetfn,'w')
hdr = 'Time,Longitude,Latitude,RMC_QUAL,SPD,COURSE,MAGVAR,GPS_FIX,NSATS,HDOP,REC_ALT,GEOID,AIR_TEMP,BARO_PRES,REL_HUM \n'
fout.write(hdr)
for m in metfiles:
	metext = m.find('_FiveMin.dat')
	gps = m[0:metext] + srch1[1:len(srch1)]
	f = open(m)
	ln = f.readline()
	ln = f.readline()
	ln = f.readline()
	ln = f.readline()
	for ln in f:
		cm = [r.start() for r in re.finditer(',',ln)]
		datestr = ln[1:cm[0]-1]
		tempstr = ln[cm[2]:cm[3]]
		barostr = ln[cm[3]:cm[4]]
		relhstr = ln[cm[8]:len(ln)-2]
		g = open(gps)
		tt = False
		for lg in g:
			tt = datestr in lg
			if tt:
				break
		if tt:
			gpsdata = readCampbellGPS(datestr,lg)
			
			pstr = gpsdata + tempstr + barostr + relhstr + ' \n'
		else:
			pstr = datestr + tempstr + barostr + relhstr + 'NaN \n'
		fout.write(pstr)
fout.close()
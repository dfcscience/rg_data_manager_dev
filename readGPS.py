#!/usr/bin/env python

import re

def readGPS(datestr,lg):
	
	dsh = [r.start() for r in re.finditer('-',datestr)]
	logday = int(datestr[dsh[1]+1:dsh[1]+3])
	# rmc data
	rmcst = lg.find('$GPRMC',0)
	rmcft = lg.find('"',rmcst)
	rmctmp = lg[rmcst:rmcft]
	cmar = [r.start() for r in re.finditer(',',rmctmp)]
	# gps time HHMMSS
	gtime = rmctmp[cmar[0]+1:cmar[1]]
	# gps quality
	tt = 'A' in rmctmp
	if tt:
		gps_qual = 'A' + ','
	else:
		gps_qual = 'V' + ','
	# latitude - convert to decimal degrees. currently only fishing in northern hemisphere
	latstr = rmctmp[cmar[2]+1:cmar[3]]
	m = latstr.find('.',0)
	latmin = latstr[m-2:len(latstr)]
	latdec = float(latstr[0:m-2]) + float(latmin)/60
	latdecstr = '%.5f' % latdec + ','
	# longitude - convert to decimal degrees
	lonstr = rmctmp[cmar[4]+1:cmar[5]]
	m = lonstr.find('.',0)
	lonmin = lonstr[m-3:len(lonstr)]
	londec = float(lonstr[0:m-2]) + float(lonmin)/60
	lonhem = rmctmp[cmar[5]+1:cmar[6]]
	h = 'W' in lonhem
	if h:
		londec = londec * -1
	londecstr = '%.5f' % londec + ','
	# speed over ground
	spd = rmctmp[cmar[6]+1:cmar[7]] + ','
	# course over ground (true)
	crs = rmctmp[cmar[7]+1:cmar[8]] + ','
	# magnetic variation
	magvar = rmctmp[cmar[9]+1:cmar[10]]
	magvarf = float(magvar)
	vardir = rmctmp[cmar[10]+1:len(rmctmp)]
	h = 'E' in vardir
	if h:
		magvarf = -1 * magvarf
	magvarstr = '%.1f' % magvarf + ','
	# gga data
	gst = lg.find('$GPGGA',0)
	gft = lg.find('"',gst)
	ggatmp = lg[gst:gft]
	cmag = [r.start() for r in re.finditer(',',ggatmp)]
	gps_fix = ggatmp[cmag[5]+1:cmag[6]] + ','
	nsats = ggatmp[cmag[6]+1:cmag[7]] + ','
	hdop = ggatmp[cmag[7]+1:cmag[8]] + ','
	gps_alt = ggatmp[cmag[8]+1:cmag[9]] + ','
	geoid = ggatmp[cmag[10]+1:cmag[11]]
	# compare gps hour to logger time
	col = [r.start() for r in re.finditer(':',datestr)]
	tdif = int(gtime[0:2]) - int(datestr[col[0]-2:col[0]]) # hour difference
	if tdif < 0:
		logday += 1
	
	if logday < 10:
		logdaystr = '0' + '%i' % logday
	else:
		logdaystr = '%i' % logday
	
	# make ISO 8601 date yyyy-mm-ddTHH:MM:SS
	yymmdd = datestr[0:dsh[1]] + '-' + logdaystr + 'T' 
	hhmmss = gtime[0:2] + ':' + gtime[2:4] + ':' + gtime[4:6]
	date8601 = yymmdd + hhmmss + ','
	
	#output
	# date8601,lon,lat,gps_qual,spd,crs,magvar,gps_fix,nsats,hdop,gps_alt,geoid
	gout = date8601+londecstr+latdecstr+gps_qual+spd+crs+magvarstr+gps_fix+nsats+hdop+gps_alt+geoid
	return(gout)
	
	
	
	
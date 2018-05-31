import re
from glob import glob
#datadir =  'C:/DATA/ARCHIVE/201805240427/'

def CombineOneSecGPS(datadir):
    hdr = 'Logger Time,GPS HHMMSS,Longitude,Latitude,RMC_QUAL,SPD,COURSE,MAGVAR,GPS_FIX,NSATS,HDOP,REC_ALT,GEOID \n'
    slh = [r.start() for r in re.finditer('/', datadir)]
    outfile = datadir + 'AKAMALIK_' + datadir[slh[2]+1:slh[3]] + '_OneSec_GPS.csv'
    fout = open(outfile,'w')
    fout.write(hdr)
    srchstr = datadir + '*OneSec.dat'
    gpsfiles = glob(srchstr)
    for g in gpsfiles:
        f = open(g)
        for x in range(5):
            ln = f.readline()
        for ln in f:
            qt = [r.start() for r in re.finditer('"', ln)]
            logstr = ln[1:qt[1]] + ','
            rmcstr = ln[qt[2]:qt[3]]
            ggastr = ln[qt[4]:qt[5]]
            # rmc data
            cmar = [r.start() for r in re.finditer(',', rmcstr)]
            gtime = rmcstr[cmar[0] + 1:cmar[1]] + ','
            tt = 'A' in rmcstr
            if tt:
                gps_qual = 'A' + ','
            else:
                gps_qual = 'V' + ','
            # latitude
            latstr = rmcstr[cmar[2] + 1:cmar[3]]
            m = latstr.find('.', 0)
            latmin = latstr[m - 2:len(latstr)]
            latdec = float(latstr[0:m - 2]) + float(latmin) / 60
            latdecstr = '%.5f' % latdec + ','
            # longitude
            lonstr = rmcstr[cmar[4] + 1:cmar[5]]
            m = lonstr.find('.', 0)
            lonmin = lonstr[m - 3:len(lonstr)]
            londec = float(lonstr[0:m - 2]) + float(lonmin) / 60
            lonhem = rmcstr[cmar[5] + 1:cmar[6]]
            h = 'W' in lonhem
            if h:
                londec = londec * -1
            londecstr = '%.5f' % londec + ','
            # speed over ground
            spd = rmcstr[cmar[6] + 1:cmar[7]] + ','
            # course over ground (true)
            crs = rmcstr[cmar[7] + 1:cmar[8]] + ','
            # magnetic variation
            magvar = rmcstr[cmar[9] + 1:cmar[10]]
            magvarf = float(magvar)
            vardir = rmcstr[cmar[10] + 1:len(rmcstr)]
            h = 'E' in vardir
            if h:
                magvarf = -1 * magvarf
            magvarstr = '%.1f' % magvarf + ','
            # gga data
            cmag = [r.start() for r in re.finditer(',', ggastr)]
            gps_fix = ggastr[cmag[5] + 1:cmag[6]] + ','
            nsats = ggastr[cmag[6] + 1:cmag[7]] + ','
            hdop = ggastr[cmag[7] + 1:cmag[8]] + ','
            gps_alt = ggastr[cmag[8] + 1:cmag[9]] + ','
            geoid = ggastr[cmag[10] + 1:cmag[11]]
            gout = logstr + gtime + londecstr + latdecstr + gps_qual + spd + crs + magvarstr + gps_fix + nsats + hdop + gps_alt + geoid + '\n'
            fout.write(gout)
        f.close()
    fout.close()
    return(outfile)
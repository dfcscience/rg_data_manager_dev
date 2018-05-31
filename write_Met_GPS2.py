import re
from glob import glob

def write_Met_GPS2(datadir,allgps):
    maxday = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    slh = [r.start() for r in re.finditer('/',datadir)]
    #wkdir = '201802012132_akamalik_CR1000'
    #basedir = '/Users/dfc/Documents/ARC/RoyalGreenland/MET/'
    #datadir = basedir + wkdir + '/'
    srch5 = '*_FiveMin.dat'
    metfiles = glob(datadir + srch5)
    fn = datadir[slh[2] + 1:slh[3]]
    allmetfn = datadir + 'AKAMALIK_' + fn + '_MET_GPS.csv'
    fout = open(allmetfn, 'w')
    hdr = 'Time,Longitude,Latitude,RMC_QUAL,SPD,COURSE,MAGVAR,GPS_FIX,NSATS,HDOP,REC_ALT,GEOID,AIR_TEMP,BARO_PRES,REL_HUM \n'
    fout.write(hdr)
    for m in metfiles:
        f = open(m)
        ln = f.readline()
        ln = f.readline()
        ln = f.readline()
        ln = f.readline()
        for ln in f:
            cm = [r.start() for r in re.finditer(',', ln)]
            datestr = ln[1:cm[0] - 1]
            tempstr = ln[cm[2]:cm[3]]
            barostr = ln[cm[3]:cm[4]]
            relhtmp = ln[cm[8]:len(ln)]
            pd = relhtmp.find('.')
            relhstr = relhtmp[0:pd+2]
            g = open(allgps)
            tt = False
            for lg in g:
                tt = datestr in lg
                if tt:
                    break
            if tt:
                #gpsdata = readGPS(datestr, lg)
                cma = [r.start() for r in re.finditer(',', lg)]
                logtime = lg[0:cma[0]]
                col = [r.start() for r in re.finditer(':', logtime)]
                dsh = [r.start() for r in re.finditer('-', logtime)]
                logmon = int(logtime[dsh[0] + 1:dsh[1]])
                md = maxday[logmon - 1]
                logday = int(logtime[dsh[1] + 1:dsh[1] + 3])
                loghr = int(logtime[col[0] - 2:col[0]])
                gtime = lg[cma[0] + 1:cma[1]]
                ghr = int(gtime[0:2])
                tdif = ghr - loghr
                if tdif < 0:
                    logday += 1
                if logday > md:
                    logday = 1
                    logmon += 1
                if logday < 10:
                    logdaystr = '0' + '%i' % logday
                else:
                    logdaystr = '%i' % logday
                if logmon < 10:
                    logmonstr = '0' + '%i' % logmon
                else:
                    logmonstr = '%i' % logmon
                logyrstr = logtime[0:dsh[0]]
                yymmdd = logyrstr + '-' + logmonstr + '-' + logdaystr
                hhmmss = gtime[0:2] + ':' + gtime[2:4] + ':' + gtime[4:6]
                date8601 = yymmdd + 'T' + hhmmss + ','
                geoid = lg[cma[11]+1:len(lg)]
                pd = geoid.find('.')
                geoidstr = geoid[0:pd + 2]
                gpsdata = lg[cma[1] + 1:cma[11]] + ',' + geoidstr
                pstr = date8601 + gpsdata + tempstr + barostr + relhstr + ' \n'
            else:
                pstr = datestr + tempstr + barostr + relhstr + 'NaN \n'
            fout.write(pstr)
    fout.close()
    return(allmetfn)
import re
from glob import glob
from readGPS import readGPS

def write_Met_GPS(datadir):
    slh = [r.start() for r in re.finditer('/',datadir)]
    #wkdir = '201802012132_akamalik_CR1000'
    #basedir = '/Users/dfc/Documents/ARC/RoyalGreenland/MET/'
    #datadir = basedir + wkdir + '/'
    srch5 = '*_FiveMin.dat'
    metfiles = glob(datadir + srch5)
    srch1 = '*_OneSec.dat'
    #gpsfiles = glob(datadir + srch1)
    fn = datadir[slh[2] + 1:slh[3]]
    allmetfn = datadir + 'AKAMALIK_' + fn + '_MET_GPS.csv'
    fout = open(allmetfn, 'w')
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
            cm = [r.start() for r in re.finditer(',', ln)]
            datestr = ln[1:cm[0] - 1]
            tempstr = ln[cm[2]:cm[3]]
            barostr = ln[cm[3]:cm[4]]
            relhtmp = ln[cm[8]:len(ln)]
            pd = relhtmp.find('.')
            relhstr = relhtmp[0:pd+2]
            g = open(gps)
            tt = False
            for lg in g:
                tt = datestr in lg
                if tt:
                    break
            if tt:
                gpsdata = readGPS(datestr, lg)
                pstr = gpsdata + tempstr + barostr + relhstr + ' \n'
            else:
                pstr = datestr + tempstr + barostr + relhstr + 'NaN \n'
            fout.write(pstr)
    fout.close()
    return(allmetfn)
import psutil, os, time, shutil, errno, zipfile, smtplib, re
from datetime import datetime
from pathlib import Path
from glob import glob
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders
# DFC functions
from DownloadComplete import DownloadComplete
from MakeFileName import MakeFileName
from CheckFileExists import CheckFileExists
from CheckNewData import CheckNewData
from CheckLoggerNet import CheckLoggerNet
from checkRBR import checkRBR
from archivedir import archivedir
from ziparchivedir import ziparchivedir
#from emaildata import emaildata
from Write2Log import Write2Log
from readGPS import readGPS
from write_Met_GPS import write_Met_GPS
from CombineOneSecGPS import CombineOneSecGPS
from upload_file_dbx import upload_file_dbx

########################################################################################################################
odir = 'C:/Campbellsci/LoggerNet/'
mdir = 'C:/DATA/'
filelist = ['CR1000_OneSec.dat','CR1000_FiveMin.dat','CR1000_DataTableInfo.dat']
ftype = '*.dat'
srchstr = mdir+ftype
localstoragedir = mdir + 'ARCHIVE/'
copydir = 'D:/METDATA/'
########################################################################################################################
# email settings
fromaddr = 'dfc.rg.datatx@gmail.com'
frompass = 'akamalikdata'
toaddr = 'danfcarlson@bios.au.dk'
########################################################################################################################
logfilename = 'C:/Python27/Akamalik_DataManager_log_%s' % datetime.now().strftime('%Y%m%d%H%M') + '.txt'
fout = open(logfilename,'w')
#fout.close()
# time interval in seconds
LN_dt = 600 #LN = LoggerNet
LN_next_check = time.time()
data_dt = 1800 # check for data every half hour
data_next_check = time.time()
zip_dt = 3600 # send data every hour
zip_next_check = time.time()
mail_timer = 360

start_time = time.time()
LN_next_check = start_time + LN_dt
data_next_check = start_time + data_dt
zip_next_check = start_time + zip_dt
debug = True

# main body of program
while True:
    # check if loggernet is running
    if time.time() > LN_next_check:
        LN_next_check += LN_dt
        #print 'Checking LoggerNet'
        userstr = ' Checking LoggerNet, ' + CheckLoggerNet()
        if debug:
            print(userstr)
        Write2Log(userstr, logfilename)
    # check for new data every hour
    if time.time() >data_next_check:
        data_next_check += data_dt
        #print 'Checking for new data'
        userstr = ' Checking for new data, %i files transferred' % CheckNewData(odir,mdir,filelist)
        if debug:
            print userstr
        Write2Log(userstr, logfilename)
    # archive data - zip_dt = 3600
    if time.time() > zip_next_check:
        zip_next_check += zip_dt
        filestoprocess = glob(srchstr)
        if len(filestoprocess)>0:
            #print 'Zipping Data'
            lastarchivedir, dirstring = archivedir(localstoragedir, filestoprocess)
            # combine all GPS
            allgps = CombineOneSecGPS(lastarchivedir)
            # combine met and GPS
            allmetfn = write_Met_GPS2(lastarchivedir,allgps)
            userstr = ' Zip files in %s' % dirstring
            if debug:
                print userstr
            Write2Log(userstr, logfilename)
            #print 'Copying to D:/METDATA/'
            copysuccess,filename = ziparchivedir(lastarchivedir, dirstring, localstoragedir,copydir,'_akamalik_CR1000')
            userstr = ' Copied to D:/METDATA/'
            if debug:
                print userstr
            Write2Log(userstr, logfilename)
            if copysuccess:
                file_from = [allmetfn,allgps]
                for ff in file_from:
                    # extract filename for dropbox
                    slh = [r.start() for r in re.finditer('/', ff)]
                    file_to = '/RG/' + ff[slh[3]+1:len(ff)]
                    upload_file_dbx(ff, file_to)
                    if debug:
                        print 'uploaded %s to dropbox' % ff

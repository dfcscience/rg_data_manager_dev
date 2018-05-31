import psutil, os, time, shutil, errno, zipfile, smtplib
from datetime import datetime
from pathlib import Path
from glob import glob

def DownloadComplete(fname):
    downcom = False
    f = open(fname)
    dd = f.read()
    nn = f.readline()
    f.close()
    if len(nn)==0:
        downcomp = True
    return(downcomp)

def MakeFileName(fname,savedir,filesuffix):
    ftime = os.path.getmtime(fname)
    d = datetime.fromtimestamp(ftime)
    newname = savedir + '%i' % d.year + '_%1.2i' % d.month + '_%1.2i' % d.day + '_%1.2i' % d.hour + '_%1.2i_' % d.minute + filesuffix
    return(newname)

def CheckNewData(cr_data):
    txsuccess = 0
    check1s = Path(cr_data[0] + cr_data[2])
    if check1s.exists():
        downcomp = DownloadComplete(cr_data[0] + cr_data[2])
        if downcomp:
            fname1s = MakeFileName(cr_data[0] + cr_data[2],cr_data[1],cr_data[2])
            try:
                os.rename(cr_data[0] + cr_data[2], fname1s)
                txsuccess += 1
            except:
                pass
    check5m = Path(cr_data[0] + cr_data[3])
    if check5m.exists():
        downcomp5 = DownloadComplete(cr_data[0] + cr_data[3])
        if downcomp5:
            fname5m = MakeFileName(cr_data[0] + cr_data[3],cr_data[1],cr_data[3])
            try:
                os.rename(cr_data[0] + cr_data[3], fname5m)
                txsuccess += 1
            except:
                pass
    checkinfo = Path(cr_data[0]+cr_data[4])
    if checkinfo.exists():
        downcompI = DownloadComplete(cr_data[0]+cr_data[4])
        if downcompI:
            fnameI = MakeFileName(cr_data[0]+cr_data[4],cr_data[1],cr_data[4])
            try:
                os.rename(cr_data[0] + cr_data[4], fnameI)
                txsuccess += 1
            except:
                pass
    return(txsuccess)

def archivedir(basedir,filelist):
    dirname = datetime.now().strftime('%Y%m%d%H%M')
    dirstring = dirname + '/'
    mydir = os.path.join(basedir,dirstring)
    try:
        os.makedirs(mydir)
        for file in filelist:
            nn = file.find('\\')
            ff = file[nn+1:]
            mvname = mydir + ff
            os.rename(file,mvname)
        return (mydir,dirname)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise # This was not a directory exist error...

def ziparchivedir(dirtozip,dirstring,zipdir,copydir,dataID):
    outputfilename = zipdir + dirstring + dataID
    shutil.make_archive(outputfilename,'zip',dirtozip)
    srchstr = outputfilename+'.zip'
    filetocopy = glob(srchstr)
    success = False
    if len(filetocopy)>0:
        try:
            shutil.copy(filetocopy[0],copydir)
            success = True
        except:
            pass
    return(success,filetocopy)
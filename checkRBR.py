import os, datetime
from glob import glob
from DownloadComplete import DownloadComplete

def checkRBR(rbr_dir,archive_dir):
    txsuccess = [0,'N','N']
    srchstr = rbr_dir + '*.rsk'
    filestoprocess = glob(srchstr)
    if len(filestoprocess)>0:
        dirname = datetime.now().strftime('%Y%m%d%H%M_CTD')
        dirstring = dirname + '/'
        mydir = os.path.join(archive_dir, dirstring)
        os.makedirs(mydir)
        for file in filestoprocess:
            dc = DownloadComplete(file)
            if dc:
                nn = file.find('\\')
                ff = file[nn + 1:]
                mvname = mydir + ff
                os.rename(file, mvname)
                txsuccess[0] += 1
    if txsuccess[0] > 0:
        txsuccess[1]=mydir
        txsuccess[2]=dirname
    return txsuccess
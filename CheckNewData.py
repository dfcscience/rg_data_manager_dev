import os
from CheckFileExists import CheckFileExists
from DownloadComplete import DownloadComplete
from MakeFileName import MakeFileName

def CheckNewData(origdir,movdir,filelist):
    txsuccess = 0
    
    for f in filelist:
        ofile = origdir + f
        checkf = CheckFileExists(ofile)
        downcomp = DownloadComplete(ofile)
        if checkf & downcomp:
            fname = MakeFileName(ofile,movdir,f)
            try:
                os.rename(ofile, fname)
                txsuccess += 1
            except:
                pass
    
    return(txsuccess)
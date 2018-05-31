import shutil
from glob import glob

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
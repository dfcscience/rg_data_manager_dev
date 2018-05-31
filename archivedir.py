import os, datetime
from datetime import datetime

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
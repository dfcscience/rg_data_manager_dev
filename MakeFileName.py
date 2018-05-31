import os
from datetime import datetime

def MakeFileName(fname,savedir,filesuffix):
    ftime = os.path.getmtime(fname)
    d = datetime.fromtimestamp(ftime)
    newname = savedir + '%i' % d.year + '_%1.2i' % d.month + '_%1.2i' % d.day + '_%1.2i' % d.hour + '_%1.2i_' % d.minute + filesuffix
    return(newname)
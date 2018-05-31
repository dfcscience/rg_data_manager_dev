def DownloadComplete(fname):
    downcom = False
    f = open(fname)
    dd = f.read()
    nn = f.readline()
    f.close()
    if len(nn)==0:
        downcomp = True
    return(downcomp)
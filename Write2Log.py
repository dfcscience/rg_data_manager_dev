from datetime import datetime

def Write2Log(userstr,logfilename):
    logstr = datetime.now().strftime('%Y%m%d%H%M ') + userstr + '\n'
    with open(logfilename,'a') as myfile:
        myfile.write(logstr)
import psutil, os

def CheckLoggerNet():
    LN_running = False
    pp = [p.info for p in psutil.process_iter(attrs=['pid', 'name']) if 'LoggerNetService' in p.info['name']]
    if len(pp) > 0:
        LN_running = True
        LNstatus = "LoggerNet running"
        return(LNstatus)
    #for pid in psutil.pids():
    #    p = psutil.Process(pid)
    #    if p.name() == 'LoggerNetService.exe':
    #        LN_running = True
    if not LN_running:
        os.startfile('C:/Program Files (x86)/Campbellsci/Loggernet/ToolBar.exe')
        LNstatus = "Starting LoggerNet"
        return(LNstatus)
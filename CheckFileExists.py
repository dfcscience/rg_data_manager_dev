from pathlib import Path

def CheckFileExists(fname):
    fexist = False
    filepath = Path(fname)
    if filepath.exists():
        fexist = True
    return(fexist)
import os

def relpath(path): #working with relatve paths with current script
    dirpath = os.path.dirname(__file__)
    return os.path.join(dirpath,path)
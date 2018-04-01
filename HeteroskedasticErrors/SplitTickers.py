import os, operator

class SplitTickers(object):
    '''
    Split tickers into two sets (active/passive).
    To do so, sort corresponding files by size and split them into two.
    '''

    def __init__(self, pathtoTrades):
        
        dirpath = os.path.abspath(pathtoTrades)
        
        # Make a generator for all file paths within dirpath
        allFiles = ( os.path.join(basedir, filename) for basedir, dirs, files in os.walk(dirpath) for filename in files)
        
        filesJointSizes = ( (path, os.path.getsize(path)) for path in allFiles )
        
        sortedFilesJointSizes = (sorted( filesJointSizes, key = operator.itemgetter(1) )).reverse()
        
        for file in sortedFilesJointSizes:
            print(file)
            
        # TODO fill dico with cumulative sizes and average. parse ticker and split into 2
        cumSize = {}
        
        
    
    def getPassiveStocks(self):
        return(self._passive)
    
    def getActiveStocks(self):
        return(self._active)
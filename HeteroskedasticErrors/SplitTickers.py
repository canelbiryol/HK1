import pandas as pd

class SplitTickers(object):
    '''
    Split tickers into two sets (active/passive).
    To do so, sort their volume means in descending order.
    '''

    def __init__(self, statsPath='/media/louis/DATA/documents/cours/NYU/SPRING_18/ATQS/HK1/stats/stats.xlsx'):
        
        # Old: Do it with file sizes. Problematic because doesn't account for empty day/tickers
        """
        dirpath = os.path.abspath(pathtoTrades)
        # Make a generator for all file paths within dirpath
        allFiles = ( os.path.join(basedir, filename) for basedir, dirs, files in os.walk(dirpath) for filename in files)
        filesJointSizes = ( (path, os.path.getsize(path)) for path in allFiles )
        sortedFilesJointSizes = (sorted( filesJointSizes, key = operator.itemgetter(1) )).reverse()
        for file in sortedFilesJointSizes:
            print(file)
        """

        xlsStats = pd.ExcelFile(statsPath)
        
        # After visual inspection
        indicesToDrop = [9, 100, 114, 137, 246, 324, 432, 444]

        pdMatrix = pd.read_excel(xlsStats, 'vol')
        self._newMat = pdMatrix.drop(pdMatrix.index[indicesToDrop])
        self._newMat.index = self._newMat['ticker']
        
        # Vol means descending
        self._means = (self.getVolMeanTickers()).sort_values(ascending=False)

        # Split into two
        self._active = (self._means.iloc[:int(len(self._means.index)/2)]).index.values
        self._passive = (self._means.iloc[int(len(self._means.index)/2):]).index.values
        
    def getVolMeanTickers(self):
        return(self._newMat.mean(axis=1))
    
    def getPassiveStocks(self):
        return(self._passive)
    
    def getActiveStocks(self):
        return(self._active)
import pandas as pd

class StatsReader(object):
    '''
    Take the statistics excel sheet path obtained with DataReadingLoop as an input.
    Reads it sheet by sheet (i.e. stat by stat) and stacks the rows of each sheet to a long
    numpy array, to be sent to OptimizeEtaBeta class.
    '''

    def __init__(self, statsPath, boolDisplay):
        xlsStats = pd.ExcelFile(statsPath)
        
        # After visual inspection
        indicesToDrop = [9, 100, 114, 137, 246, 324, 432, 444]
        
        # Instantiate attributes
        self._arrivalprice = self.toVector(pd.read_excel(xlsStats, 'arrival_price'), indicesToDrop, boolDisplay).astype(float)
        self._imbalance = self.toVector(pd.read_excel(xlsStats, 'imbalance'), indicesToDrop, boolDisplay).astype(float)
        self._terminalprice = self.toVector(pd.read_excel(xlsStats, 'terminal_price'), indicesToDrop, boolDisplay).astype(float)
        self._VWAPuntil330 = self.toVector(pd.read_excel(xlsStats, 'VWAPuntil330'), indicesToDrop, boolDisplay).astype(float)
        self._VWAPuntil400 = self.toVector(pd.read_excel(xlsStats, 'VWAPuntil400'), indicesToDrop, boolDisplay).astype(float)
        self._vol = self.toVector(pd.read_excel(xlsStats, 'vol'), indicesToDrop, boolDisplay).astype(float)
        self._imbalancevalue = self.toVector(pd.read_excel(xlsStats, 'imbalance_value'), indicesToDrop, boolDisplay).astype(float)
        self._std2minutereturn = self.toVector(pd.read_excel(xlsStats, 'std_2_min_returns'), indicesToDrop, boolDisplay).astype(float)
        # To add if 2 minute returns needed
        #self._2minutereturn = self.toVector(pd.read_excel(xlsStats, '2_minute_returns'), indicesToDrop, boolDisplay).astype(ndarray)

    # Flattens a pandas dataframe to a big vector
    def toVector(self, pdMatrix, indicesDropped, display=False):
        newMat = pdMatrix.drop(pdMatrix.index[indicesDropped])
        newMat.index = range(len(newMat))
        if display:
            print(newMat)
            
        return((newMat.drop(['ticker'], axis=1)).values.flatten())

    # Getters
    def getArrivalPriceVector(self):
        return(self._arrivalprice)

    def getImbalanceVector(self):
        return(self._imbalance)

    def getVWAPuntil330Vector(self):
        return(self._VWAPuntil330)

    def getVWAPuntil400Vector(self):
        return(self._VWAPuntil400)

    def getVolVector(self):
        return(self._vol)

    def getImbalanceValueVector(self):
        return(self._imbalancevalue)

    def getSTD2minRetVector(self):
        return(self._std2minutereturn)

    # To add if 2 minute returns needed
    #def get2minRetArraysVector(self):
        #return(self._2minutereturn)
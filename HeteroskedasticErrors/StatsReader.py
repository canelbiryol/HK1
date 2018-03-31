import pandas as pd
from numpy import ndarray

class StatsReader(object):
    '''
    Take the statistics excel sheet path obtained with DataReadingLoop as an input.
    Reads it sheet by sheet (i.e. stat by stat) and stacks the rows of each sheet to a long
    numpy array, to be sent to OptimizeEtaBeta class.
    '''

    def __init__(self, statsPath):
        xlsStats = pd.ExcelFile(statsPath)
        
        # Instantiate attributes
        self._arrivalprice = self.toVector(pd.read_excel(xlsStats, 'arrival_price')).astype(float)
        self._imbalance = self.toVector(pd.read_excel(xlsStats, 'imbalance')).astype(float)
        self._terminalprice = self.toVector(pd.read_excel(xlsStats, 'terminal_price')).astype(float)
        self._VWAPuntil330 = self.toVector(pd.read_excel(xlsStats, 'VWAPuntil330')).astype(float)
        self._VWAPuntil400 = self.toVector(pd.read_excel(xlsStats, 'VWAPuntil400')).astype(float)
        self._vol = self.toVector(pd.read_excel(xlsStats, 'vol')).astype(float)
        self._imbalancevalue = self.toVector(pd.read_excel(xlsStats, 'imbalance_value')).astype(float)
        self._2minutereturn = self.toVector(pd.read_excel(xlsStats, '2_minute_returns')).astype(ndarray)
        self._std2minutereturn = self.toVector(pd.read_excel(xlsStats, 'std_2_min_returns')).astype(float)
    
    # Flattens a pandas dataframe to a big vector
    def toVector(self, pdMatrix):
        return((pdMatrix.drop(['ticker'], axis=1)).values.flatten())

    # Getters
    def getArrivalPriceVector(self):
        return(self._arrivalprice)

    def getImbalanceVector(self):
        return(self._arrivalprice)

    def getVWAPuntil330Vector(self):
        return(self._VWAPuntil330)

    def getVWAPuntil400Vector(self):
        return(self._VWAPuntil400)

    def getVolVector(self):
        return(self._vol)

    def getImbalanceValueVector(self):
        return(self._imbalancevalue)

    def get2minRetArraysVector(self):
        return(self._2minutereturn)

    def getSTD2minRetVector(self):
        return(self._std2minutereturn)
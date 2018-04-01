import pandas as pd
import numpy as np
from math import sqrt

class StatsReader(object):
    '''
    Take the statistics excel sheet path obtained with DataReadingLoop as an input.
    Reads it sheet by sheet (i.e. stat by stat) and stacks the rows of each sheet to a long
    numpy array, to be sent to OptimizeEtaBeta class.
    '''

    def __init__(self, statsPath, boolDisplay):
        self._xlsStats = pd.ExcelFile(statsPath)
        
        # After visual inspection
        indicesToDrop = self.getIndicesToDrop()

        # Instantiate attributes
        self._arrivalprice = self.toVector(pd.read_excel(self._xlsStats, 'arrival_price'), indicesToDrop, boolDisplay).astype(float)
        self._imbalance = self.toVector(pd.read_excel(self._xlsStats, 'imbalance'), indicesToDrop, boolDisplay).astype(float)
        self._terminalprice = self.toVector(pd.read_excel(self._xlsStats, 'terminal_price'), indicesToDrop, boolDisplay).astype(float)
        self._VWAPuntil330 = self.toVector(pd.read_excel(self._xlsStats, 'VWAPuntil330'), indicesToDrop, boolDisplay).astype(float)
        self._VWAPuntil400 = self.toVector(pd.read_excel(self._xlsStats, 'VWAPuntil400'), indicesToDrop, boolDisplay).astype(float)
        self._vol = self.toVector(pd.read_excel(self._xlsStats, 'vol'), indicesToDrop, boolDisplay).astype(float)
        self._imbalancevalue = self.toVector(pd.read_excel(self._xlsStats, 'imbalance_value'), indicesToDrop, boolDisplay).astype(float)
        self._std2minutereturn = self.toVector(pd.read_excel(self._xlsStats, 'std_2_min_returns'), indicesToDrop, boolDisplay).astype(float)
        # To add if 2 minute returns needed
        #self._2minutereturn = self.toVector(pd.read_excel(self._xlsStats, '2_minute_returns'), indicesToDrop, boolDisplay).astype(ndarray)

    # Get indices of all rows of all sheets containing NaN
    def getIndicesToDrop(self):
        
        inds = np.where(np.asanyarray(np.isnan((pd.read_excel(self._xlsStats, 'arrival_price').values[:,1:]).astype(float))))[0]
        inds = np.concatenate((inds, np.array(np.where(np.asanyarray(np.isnan((pd.read_excel(self._xlsStats, 'imbalance').values[:,1:]).astype(float))))[0])),0)
        inds = np.concatenate((inds, np.array(np.where(np.asanyarray(np.isnan((pd.read_excel(self._xlsStats, 'terminal_price').values[:,1:]).astype(float)))))[0]),0)
        inds = np.concatenate((inds, np.array(np.where(np.asanyarray(np.isnan((pd.read_excel(self._xlsStats, 'VWAPuntil330').values[:,1:]).astype(float)))))[0]),0)
        inds = np.concatenate((inds, np.array(np.where(np.asanyarray(np.isnan((pd.read_excel(self._xlsStats, 'VWAPuntil400').values[:,1:]).astype(float)))))[0]),0)
        inds = np.concatenate((inds, np.array(np.where(np.asanyarray(np.isnan((pd.read_excel(self._xlsStats, 'vol').values[:,1:]).astype(float)))))[0]),0)
        inds = np.concatenate((inds, np.array(np.where(np.asanyarray(np.isnan((pd.read_excel(self._xlsStats, 'imbalance_value').values[:,1:]).astype(float)))))[0]),0)
        inds = np.concatenate((inds, np.array(np.where(np.asanyarray(np.isnan((pd.read_excel(self._xlsStats, 'std_2_min_returns').values[:,1:]).astype(float)))))[0]),0)

        inds = np.unique(inds)
        return(inds)
    
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

    def getTerminalPriceVector(self):
        return(self._terminalprice)

    def getVWAPuntil330Vector(self):
        return(self._VWAPuntil330)

    def getVWAPuntil400Vector(self):
        return(self._VWAPuntil400)

    def getVolVector(self):
        return(self._vol)

    def getVolMeanTickers(self):
        return(self._newMat.mean(axis=1))

    def getImbalanceValueVector(self):
        return(self._imbalancevalue)

    def getSTD2minRetVector(self):
        return(self._std2minutereturn)
    
    # Average Daily Values (10 days loopback)
    def getADValuesVector(self):
        mat = self._vol * self._VWAPuntil400
        roll = self.rollingWindow(mat,10)
        
        d = []
        for i in range(0,9):
            newWindow = [mat[j] for j in range(0,i+1)]
            d.append(newWindow)
        d = d + list(roll)

        return(np.array([np.mean(x) for x in d]))

    # Average Daily Volumes (10 days loopback)
    def getADVolVector(self):
        roll = self.rollingWindow(self._vol,10)
        
        d = []
        for i in range(0,9):
            newWindow = [self._vol[j] for j in range(0,i+1)]
            d.append(newWindow)
        d = d + list(roll)

        return(np.array([np.mean(x) for x in d]))

    # Sigmas (10 days loopback)
    def getStdErrorVector(self):
        roll = self.rollingWindow(self._std2minutereturn,10)
        
        d = []
        for i in range(0,9):
            newWindow = [self._std2minutereturn[j] for j in range(0,i+1)]
            d.append(newWindow)
        d = d + list(roll)
        
        average_std = lambda xarr: sqrt(sum(np.power(xarr, 2))/len(xarr))

        return(np.array([average_std(arr) for arr in d]))
    
    # Auxiliary function to get 10 days windows
    def rollingWindow(self, a, window):
        
        window = min(a.shape[-1], window)
        shape = a.shape[:-1] + (a.shape[-1] - window + 1, window)
        strides = a.strides + (a.strides[-1],)
        
        return np.lib.stride_tricks.as_strided(a, shape=shape, strides=strides)

    # To add if 2 minute returns needed
    #def get2minRetArraysVector(self):
        #return(self._2minutereturn)
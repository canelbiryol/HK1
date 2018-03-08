import numpy as np
import math
from _collections import deque

class TAQCleaner(object):
    '''
    Cleans an array of TAQ Data.
    The method gives the option to store the cleaned data to files.
    Default values for k and gamma were those given by the simulation (cf. CleanCalibration.py)
    '''

    def __init__(self, stackedQuotes, stackedTrades, kT=45, gammaT=0.02, kQ=55, gammaQ=0.0175):
        '''
        Constructor: initialize attributes
        '''
        # Instantiate attributes
        self._quotes = stackedQuotes
        self._trades = stackedTrades
        
        # Suggested initial parameters, to calibrate
        self._kT = kT
        self._gammaT = gammaT
        self._kQ = kQ
        self._gammaQ = gammaQ

    def cleanQuotesIndices(self):
        # toRemove will keep track of indices to remove
        length = self._quotes.shape[0]
        toRemove = deque()
        i = 0
        
        # Rolling parameters
        rollMeanMid = 0
        rollStdMid = 0
        
        # BROWNLEES AND GALLO SUGGESTION (unused, we followed the assignment guidelines)
        # Min price difference in the timeframe 
        # It is likely to be the resolution parameter for the stock given the high number of transactions
        #askIncrements = np.array(self._quotes[1:length,-2].astype(np.float)) - np.array(self._quotes[0:length-1,-2].astype(np.float))
        #bidIncrements = np.array(self._quotes[1:length,-4].astype(np.float)) - np.array(self._quotes[0:length-1,-4].astype(np.float))
        #minTickDiff = min(abs(np.min(askIncrements)), abs(np.min(bidIncrements)))
        
        # Midpoints
        midList = 0.5 * (np.array(self._quotes[0:length,-4].astype(np.float)) - np.array(self._quotes[0:length,-2].astype(np.float)))
        
        for i in range(0,length):
            leftIndex = math.floor(i - self._kQ / 2)
            rightIndex = math.floor(i + self._kQ / 2)
            
            # Set bounds of the rolling windows, taking into account limit cases
            if (leftIndex < 0):
                rightIndex -= leftIndex
                leftIndex = 0
            elif (rightIndex - length >= 0):
                leftIndex -= (rightIndex - length)
                rightIndex = length
            
            # Compute rolling metrics
            rollMeanMid = np.mean(midList[leftIndex:rightIndex])
            rollStdMid = np.std(midList[leftIndex:rightIndex])

            # Test criterion
            if (abs(midList[i] - rollMeanMid) >= 2 * rollStdMid + self._gammaQ * rollMeanMid):
                toRemove.append(i)
                    
        npytoRemove = np.array(toRemove)
        npytoRemove = npytoRemove.astype(int)
        npytoRemove = np.unique(npytoRemove)
        npytoRemove = np.sort(npytoRemove)
        npytoRemove = np.flip(npytoRemove, axis=0)
        return(npytoRemove)
                    
    def cleanTradesIndices(self):
        # toRemove will keep track of indices to remove
        length = self._trades.shape[0]
        toRemove = deque()
        i = 0
        
        # Rolling parameters
        rollMean = 0
        rollStd = 0
        
        # BROWNLEES AND GALLO SUGGESTION (unused, we followed the assignment guidelines)
        # Min price difference in the timeframe 
        # It is likely to be the resolution parameter for the stock given the high number of transactions
        #tradeIncrements = np.array(self._trades[1:length,-2].astype(np.float)) - np.array(self._trades[0:length-1,-2].astype(np.float))
        #minTickDiff = abs(np.min(tradeIncrements))

        windowTrade = np.array(self._trades[0:length,-2].astype(np.float))
        
        for i in range(0,length):
            leftIndex = math.floor(i - self._kT / 2)
            rightIndex = math.floor(i + self._kT / 2)
            
            # Set bounds of the rolling windows, taking into account limit cases
            if (leftIndex < 0):
                rightIndex -= leftIndex
                leftIndex = 0
            elif (rightIndex - length >= 0):
                leftIndex -= (rightIndex - length)
                rightIndex = length

            # Compute rolling metrics
            rollMean = np.mean(windowTrade[leftIndex:rightIndex])
            rollStd = np.std(windowTrade[leftIndex:rightIndex])

            # Test criterion
            if (abs(windowTrade[i] - rollMean) >= 2 * rollStd + self._gammaT * rollMean):
                toRemove.append(i)

        npytoRemove = np.array(toRemove)
        npytoRemove = npytoRemove.astype(int)
        npytoRemove = np.unique(npytoRemove)
        npytoRemove = np.sort(npytoRemove)
        npytoRemove = np.flip(npytoRemove, axis=0)
        return(npytoRemove)
        
    def storeCleanedTrades(self, trades, directory):
        print("TODO")
        
    def storeCleanedQuotes(self, quotes, directory):
        print("TODO")
        
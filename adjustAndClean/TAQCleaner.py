import numpy as np
import math
from _collections import deque

class TAQCleaner(object):
    '''
    Cleans an array of TAQ Data.
    The method gives the option to store the cleaned data to files.
    Default values for k and gamma were those given by the simulation (cf. CleanCalibration.py)
    '''

    def __init__(self, stackedQuotes, stackedTrades, k=45, gamma=0.02):
        '''
        Constructor: initialize attributes
        '''
        # Instantiate attributes
        self._quotes = stackedQuotes
        self._trades = stackedTrades
        
        # Suggested initial parameters, to calibrate
        self._k = k
        self._gamma = gamma

    def cleanQuotesIndices(self):
        # toRemove will keep track of indices to remove
        length = self._quotes.shape[0]
        toRemove = deque()
        i = 0
        
        # Rolling parameters
        rollWindowMid = np.array([])
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
            leftIndex = math.floor(i - self._k / 2)
            rightIndex = math.floor(i + self._k / 2)
            
            # Set bounds of the rolling windows, taking into account limit cases
            if (leftIndex < 0):
                rightIndex -= leftIndex
                leftIndex = 0
            elif (rightIndex - length >= 0):
                leftIndex -= (rightIndex - length)
                rightIndex = length
            
            # Compute rolling metrics
            rollWindowMid = midList[leftIndex:rightIndex]
            rollMeanMid = np.mean(rollWindowMid)
            rollStdMid = np.std(rollWindowMid)

            # Test criterion
            for j in range(0, self._k):
                if (abs(rollWindowMid[j] - rollMeanMid) >= 2 * rollStdMid + self._gamma * rollMeanMid):
                    toRemove.append(leftIndex + j)
                    
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
        rollWindow = np.array([])
        rollMean = 0
        rollStd = 0
        
        # BROWNLEES AND GALLO SUGGESTION (unused, we followed the assignment guidelines)
        # Min price difference in the timeframe 
        # It is likely to be the resolution parameter for the stock given the high number of transactions
        #tradeIncrements = np.array(self._trades[1:length,-2].astype(np.float)) - np.array(self._trades[0:length-1,-2].astype(np.float))
        #minTickDiff = abs(np.min(tradeIncrements))

        windowTrade = np.array(self._trades[0:length,-2].astype(np.float))
        
        for i in range(0,length):
            leftIndex = math.floor(i - self._k / 2)
            rightIndex = math.floor(i + self._k / 2)
            
            # Set bounds of the rolling windows, taking into account limit cases
            if (leftIndex < 0):
                rightIndex -= leftIndex
                leftIndex = 0
            elif (rightIndex - length >= 0):
                leftIndex -= (rightIndex - length)
                rightIndex = length

            # Compute rolling metrics
            rollWindow = windowTrade[leftIndex:rightIndex]
            rollMean = np.mean(rollWindow)
            rollStd = np.std(rollWindow)

            # Test criterion
            for j in range(0, self._k):
                if (abs(rollWindow[j] - rollMean) >= 2 * rollStd + self._gamma * rollMean):
                    toRemove.append(leftIndex + j)

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
        
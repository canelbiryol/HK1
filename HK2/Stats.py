'''
Created on Apr 3, 2018

@author: canelbiryol
'''
import numpy as np
from numpy import floor
from impactModel.TickTest import TickTest

class Stats(object):
    '''
    classdocs
    '''
    def __init__(self, trades, quotes):
        '''
        Constructor
        '''
        self._trades = trades
        self._quotes = quotes
         
    def getXMinMidQuoteRet(self, delta):
        data = self._quotes
        nRecs = len(data) 
        lastMidQuote = (float(data[0][2]) + float(data[0][4])) / 2 
        
        startTS = 19 * 60 * 60 * 1000 / 2
        endTS = 16 * 60 * 60 * 1000
        numBuckets = int((endTS - startTS) / delta)
    
        midQuoteReturns = [None] * numBuckets
        iBucket = -1 # The 0th bucket
        
        # midQuoteReturns = []
        for startI in range( 1, nRecs ):
            timestamp = int(data[startI][1]) 
            # Are we past the end of good data?
            if timestamp >= endTS:
                # Yes, we are past the end of good data
                # Stop computing data buckets
                break
            # No we are not pas the end of good data
            # Are we still iterating over data that appears before
            #   the specified start of good data?
            if timestamp < startTS:
                # Yes, we have to skip this data
                continue
              
            newBucket = int( floor( ( timestamp - startTS ) / delta ) )
            if iBucket != newBucket:
                # This is a new bucket
                
                midQuote = (float(data[startI][2]) + float(data[startI][4])) / 2 
                midQuoteReturns[ newBucket ] = (midQuote / lastMidQuote) - 1
                
                # Save our new bucket count
                iBucket = newBucket
                lastMidQuote = midQuote
        return midQuoteReturns
    
    def getSTDXMinMidQuoteRet(self, midquoteReturns):
        return np.std(filter(None,midquoteReturns)) * np.sqrt(252 * 30 * 13 / 2) #annualize the 2 min returns
    
    # compute total daily vol 
    def getTotalDailyVol(self):
        
        return int(np.sum([d[1] for d in self._trades]))
    
    # compute arrival price - average of first five mid-quote prices 
    def getArrivalPrice(self, n):
        data = self._quotes
        midquotes = [None] * n
    
        for i in range(n):
            midquotes[i] = (data[i][2] + data[i][4]) / 2 
    
        return np.mean(midquotes)
    
    # compute terminal price - average of last 5 mid-quote prices
    def getTerminalPrice(self, n):
        data = self._quotes
        midquotes = [None] * n
        
        for i in range(n):
            midquotes[i] = (data[-(i+1)][2] + data[-(i+1)][4]) / 2
    
        return np.mean(midquotes)
    
    # compute volume weighted average price
    def getVWAP(self, startTS, endTS):
        data = self._trades
        v = 0
        s = 0
        counter = 0
        for i in range( 0, len(data) ):
            if( float(data[i][1]) < startTS ):
                continue
            if( float(data[i][1]) >= endTS ):
                break
            
            counter = counter + 1
            v = v + ( data[i][2] * data[i][3] )
            s = s + data[i][3]
        
        return v / s

    
    # compute imbalance using the modified TickTest from impactModel
    def getImbalance(self, startTs, endTs):
        data = self._trades
        tickTest = TickTest()
        classifications = tickTest.classifyAll( data, startTs, endTs )
        
        imbalance = sum([ c[1] * c[2] for c in classifications])
        return imbalance

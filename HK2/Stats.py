'''
Created on Apr 3, 2018

@author: canelbiryol
'''
import numpy as np
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
        lastTs = int(data[0][1])
        lastMidQuote = (float(data[0][2]) + float(data[0][4])) / 2 
        
        midQuoteReturns = []
        for startI in range( 1, nRecs ):
            timestamp = int(data[startI][1])       
                
            # check this
            if timestamp > (lastTs + delta): 
                midQuote = (float(data[startI][2]) + float(data[startI][4])) / 2 
                midQuoteReturns.append( (midQuote / lastMidQuote) - 1 )
                lastTs = lastTs + delta
                lastMidQuote = midQuote
    
        return midQuoteReturns
    
    def getSTDXMinMidQuoteRet(self, midquoteReturns):
        return np.std(midquoteReturns) * np.sqrt(252 * 30 * 13 / 2) #annualize the 2 min returns
    
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

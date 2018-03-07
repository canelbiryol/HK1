'''
Created on Mar 7, 2018

@author: Michael
'''
import numpy as np
from collections import deque

def getXSecondTradeReturns(data, seconds):
    delta = 1000 * seconds
        
    nRecs = len(data)
    lastTs = data[0][2]
    lasteDate = data[0][0]
    lastPrice = data[0][3]
    TradeReturns = deque()
    
    for startI in range( 1, nRecs ):
        timestamp = data[startI] startI )
            
        # check this
        if timestamp > (lastTs + delta):
            lastTs = lastTs + delta
            newPrice = data.getPrice( startI )
                
            TradeReturns.append( np.log(newPrice/lastPrice) )
            lastPrice = newPrice
            lastTs = timestamp
        
    return TradeReturns

def getXSecondMidQuoteReturns(data, seconds):
    delta = 1000 * seconds
        
    nRecs = data.getN()
    lastTs = data.getTimestamp(0)
    lastMidQuote = (data.getAskPrice( 0 ) + data.getBidPrice( 0 ))  / 2 
    midQuoteReturns = []
    for startI in range( 1, nRecs ):
        timestamp = data.getTimestamp( startI )
            
        # check this
        if timestamp > (lastTs + delta):
            lastTs = lastTs + delta
            #askPrice = data.getAskPrice( startI )
            #bidPrice = data.getBidPrice( startI ) 
            midQuote = (data.getAskPrice( startI ) + data.getBidPrice( startI ))  / 2 
            
            midQuoteReturns.append( np.log(midQuote/lastMidQuote) )
            lastMidQuote = midQuote
            lastTs = timestamp
        
    return midQuoteReturns

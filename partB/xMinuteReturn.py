import numpy as np
import time
import datetime

def dateStringToTS(dateString):
    return time.mktime(datetime.datetime.strptime(str(dateString), "%Y%m%d").timetuple())

def getXSecTradeReturns(data, delta):
    nRecs = len(data)
    tradeReturns = []
    timestamps = []
    
    lastTs = dateStringToTS(int(data[0][0])) + ( int(data[0][1]) / 1000 )
    lastPrice = float(data[0][2])

    for startI in range( 1, nRecs ):
        timestamp = dateStringToTS(int(data[startI][0])) + ( int(data[startI][1]) / 1000 )
        price = float(data[startI][2])
            
        # check this
        if timestamp > (lastTs + delta): 
            tradeReturns.append( (price / lastPrice) - 1 )
            lastTs = lastTs + delta
            timestamps.append(lastTs)
            lastPrice = price
        
    return [tradeReturns, timestamps]

# [DATE, TICKER, TIMESTAMP, BIDPRICE, BIDSIZE, ASKPRICE, ASKSIZE]

def getXSecMidQuoteReturns(data, delta): 
    nRecs = len(data) 
    lastTs = dateStringToTS(int(data[0][0])) + ( int(data[0][1]) / 1000 )
    lastMidQuote = (float(data[0][2]) + float(data[0][4])) / 2 
    
    #lastMidQuote = (data.getAskPrice( 0 ) + data.getBidPrice( 0 ))  / 2 
    midQuoteReturns = [] 
    timestamps = []
    for startI in range( 1, nRecs ):
        timestamp = dateStringToTS(int(data[startI][0])) + ( int(data[startI][1]) / 1000 )
        midQuote = (float(data[startI][2]) + float(data[startI][4])) / 2        
            
        # check this
        if timestamp > (lastTs + delta): 
            midQuoteReturns.append( (midQuote / lastMidQuote) - 1 )
            lastTs = lastTs + delta
            timestamps.append(lastTs)
            lastMidQuote = midQuote
            
    return [midQuoteReturns, timestamps]

import numpy as np
import time
import datetime

def dateStringToTS(dateString):
    return time.mktime(datetime.datetime.strptime(str(dateString), "%Y%m%d").timetuple())

def getXSecTradeReturns(data, delta):
    nRecs = len(data)
    tradeReturns = []
    timestamps = []
    
    lastTs = dateStringToTS(int(data[0][0])) + ( int(data[0][2]) / 1000 )
    lastPrice = float(data[0][3])

    for startI in range( 1, nRecs ):
        timestamp = dateStringToTS(int(data[startI][0])) + ( int(data[startI][2]) / 1000 )
        price = float(data[startI][3])
            
        # check this
        if timestamp > (lastTs + delta): 
            tradeReturns.append( (price / lastPrice) - 1 )
            timestamps.append(timestamp)
            lastTs = timestamp
            lastPrice = price
        
    return [tradeReturns, timestamps]

# [DATE, TICKER, TIMESTAMP, BIDPRICE, BIDSIZE, ASKPRICE, ASKSIZE]

def getXSecMidQuoteReturns(data, delta): 
    nRecs = len(data) 
    lastTs = dateStringToTS(int(data[0][0])) + ( int(data[0][2]) / 1000 )
    lastMidQuote = (float(data[0][3]) + float(data[0][5])) / 2 
    
    #lastMidQuote = (data.getAskPrice( 0 ) + data.getBidPrice( 0 ))  / 2 
    midQuoteReturns = [] 
    timestamps = []
    for startI in range( 1, nRecs ):
        timestamp = dateStringToTS(int(data[startI][0])) + ( int(data[startI][2]) / 1000 )
        midQuote = (float(data[startI][3]) + float(data[startI][5])) / 2        
            
        # check this
        if timestamp > (lastTs + delta): 
            midQuoteReturns.append( (midQuote / lastMidQuote) - 1 )
            timestamps.append(timestamp)
            lastTs = timestamp
            lastMidQuote = midQuote
            
    return [midQuoteReturns, timestamps]

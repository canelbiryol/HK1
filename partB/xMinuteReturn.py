import numpy as np
from numpy import floor
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
    
     # Save start and end times
    numBuckets = 195
    startTS = 19 * 60 * 60 * 1000 / 2
    endTS = 16 * 60 * 60 * 1000
        
    bucketLen = (endTS - startTS) / numBuckets
    
    timestamps = [None] * numBuckets
    midQuoteReturns = [None] * numBuckets
    iBucket = -1 # The 0th bucket
    
    #lastMidQuote = (data.getAskPrice( 0 ) + data.getBidPrice( 0 ))  / 2 
    midQuoteReturns = [] 
    timestamps = []
    for startI in range( 1, nRecs ):
        ts = int(data[startI][1]) / 1000
        # Are we past the end of good data?
        if ts >= endTS:
            # Yes, we are past the end of good data
            # Stop computing data buckets
            break
        # No we are not pas the end of good data
        # Are we still iterating over data that appears before
        #   the specified start of good data?
        if ts < startTS:
            # Yes, we have to skip this data
            continue
        
        timestamp = dateStringToTS(int(data[startI][0])) + ts

        
        midQuote = (float(data[startI][2]) + float(data[startI][4])) / 2        
        newBucket = int( floor( ( timestamp - startTS ) / bucketLen ) )
        if iBucket != newBucket:
            # This is a new bucket
                
            # Append the first value of the new bucket
            timestamps[ newBucket ] = timestamp
            midQuoteReturns[ newBucket ] = (midQuote / lastMidQuote) - 1
                
            # Save our new bucket count
            iBucket = newBucket
            
    return [midQuoteReturns, timestamps]

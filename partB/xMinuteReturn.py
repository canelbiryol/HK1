import numpy as np

def getXSecTradeReturns(data, seconds):
    delta = 1000 * seconds
        
    nRecs = len(data)
    tradeReturns = []
    
    lastDate = int(data[0][0])
    lastTs = int(data[0][2])
    lastPrice = float(data[0][3])

    for startI in range( 1, nRecs ):
        date = int(data[startI][0])
        timestamp = int(data[startI][2])
        price = float(data[startI][3])
            
        # check this
        if timestamp > (lastTs + delta) or date > lastDate: 
            tradeReturns.append( (price / lastPrice) - 1 )
            lastDate = date
            lastTs = timestamp
            lastPrice = price
        
    return tradeReturns

# [DATE, TICKER, TIMESTAMP, BIDPRICE, BIDSIZE, ASKPRICE, ASKSIZE]

def getXSecMidQuoteReturns(data, seconds):
    delta = 1000 * seconds
        
    nRecs = len(data)
    lastDate = int(data[0][0])
    lastTs = int(data[0][2])
    lastMidQuote = (float(data[0][3]) + float(data[0][5])) / 2 
    
    #lastMidQuote = (data.getAskPrice( 0 ) + data.getBidPrice( 0 ))  / 2 
    midQuoteReturns = []
    for startI in range( 1, nRecs ):
        date = int(data[startI][0])
        timestamp = int(data[startI][2])
        midQuote = (float(data[startI][3]) + float(data[startI][5])) / 2
            
        # check this
        if timestamp > (lastTs + delta) or date > lastDate: 
            midQuoteReturns.append( (midQuote / lastMidQuote) - 1 )
            lastDate = date
            lastTs = timestamp
            lastMidQuote = midQuote
            
    return midQuoteReturns

import numpy as np
from astropy.stats import median_absolute_deviation
from scipy.stats import skew, kurtosis
import heapq
from partB.xMinuteReturn import getXSecTradeReturns, getXSecMidQuoteReturns

class TAQStats(object):
    '''
    This class calculates the basic statistics for Trade and Mid-Quote Returns.
    '''

    def __init__( self, trades, quotes, seconds):
        self._trades = trades
        self._quotes = quotes
        tradeReturns = getXSecTradeReturns(self._trades, seconds)
        self._tradeReturns = tradeReturns[0]
        self._tradeTimestamps= tradeReturns[1]        
        midQuoteReturns = getXSecMidQuoteReturns(self._quotes, seconds)
        self._quoteReturns = midQuoteReturns[0]
        self._quoteTimestamps = midQuoteReturns[1]

    # Get unique dates in Trades data
    def getTradeDates(self):
        return [date for date in set(i[0] for i in self._trades)]
    
    # Get unique dates in Quotes data
    def getQuotesDates(self):
        return [date for date in set(i[0] for i in self._quotes)]
    
    # Get number of days in the data for a ticker
    def getSampleLength(self):
        return len(self.getTradeDates())
  
    # Get N Trades
    def getNumofTrades(self):
        return len(self._trades)
  
    # Get N Quotes
    def getNumofQuotes(self):
        return len(self._quotes)
    
    # Calc friction of N Trades to N Quotes
    def getTradestoQuotes(self):
        if not self.getNumofQuotes():
            return -1
        return self.getNumofTrades() / self.getNumofQuotes()

    # Get Trade Returns  
    def getTradeReturns(self):
        return self._tradeReturns
    
    # Get timestamps for Trade Returns for plotting
    def getTradeReturnsTimestamps(self):
        return self._tradeTimestamps
    
    # Get Mid-Quote Returns
    def getMidQuoteReturns(self):
        return self._quoteReturns
    
    # Get timestamps for Mid-Quote Returns for plotting
    def getMidQuoteReturnsTimestamps(self):
        return self._quoteTimestamps
    
    # Mean Returns
    # Check annualization
    def _getMeanReturns(self, data):
        return np.mean( data ) 
    
    def getTradeMeanReturns(self):
        return np.mean(self._tradeReturns) * ( 252 / len(self.getTradeDates()) )

    def getQuoteMeanReturns(self):
        return  np.mean(self._quoteReturns) * ( 252 / len(self.getQuotesDates()) )
    
    #Median Returns
    def getTradeMedianReturns(self):
        return np.median(self._tradeReturns) * ( 252 / len(self.getTradeDates()) )

    def getQuoteMedianReturns(self):
        return np.median(self._quoteReturns) * ( 252 / len(self.getQuotesDates()) )
    
    # Std Deviations
    # Check annualization
    def _getStdReturns(self, data):
        return np.std( data ) 
    
    def getTradeStdReturns(self):
        return self._getStdReturns(self._tradeReturns) * np.sqrt(( 252 / len(self.getTradeDates())))

    def getMidQuoteStdReturns(self):
        return self._getStdReturns(self._quoteReturns) * np.sqrt(( 252 / len(self.getQuotesDates())))
     
     
    # Median Absolute Deviation
    def getTradeMedianAbsDev(self):
        return median_absolute_deviation( self._tradeReturns ) * ( 252 / len(self.getTradeDates()))
    
    def getMidQuoteMedianAbsDev(self):
        return median_absolute_deviation( self._quoteReturns ) * ( 252 / len(self.getQuotesDates()))
     
    # Skew
    def getTradeSkew(self):
        return skew( self._tradeReturns ) * ( 252 / len(self.getTradeDates()))
    
    def getMidQuoteSkew(self):
        return skew( self._quoteReturns ) * ( 252 / len(self.getQuotesDates()))
    
    # Kurtosis 
    def getTradeKurtosis(self):
        return kurtosis( self._tradeReturns ) * ( 252 / len(self.getTradeDates()))
    
    def getMidQuoteKurtosis(self):
        return kurtosis( self._quoteReturns ) * ( 252 / len(self.getQuotesDates()))
    
    # 10 Largest Returns
    def get10largestTrade(self):
        return heapq.nlargest(10, self._tradeReturns )
     
    def get10largestMidQuote(self):
        return heapq.nlargest(10, self._quoteReturns )
    
    # 10 Smallest Return
    def get10smallestTrade(self):
        return heapq.nsmallest(10, self._tradeReturns )
    
    def get10smallestMidQuote(self):
        return heapq.nsmallest(10, self._quoteReturns )
   
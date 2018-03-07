import numpy as np
from dbReaders.TAQTradesReader import TAQTradesReader
from dbReaders.TAQQuotesReader import TAQQuotesReader
from astropy.stats import median_absolute_deviation
from impactModel.FileManager import FileManager
from scipy.stats import skew, kurtosis
import heapq
from partB.xMinuteReturn import getXSecTradeReturns, getXSecMidQuoteReturns

class TAQStats(object):
    '''
    This class calculates the volume weighted average price between
    a start time and an end time (exclusive).
    '''

    def __init__( self, trades, quotes):
        '''
        This does all the processing and gives the client access to the
        results via getter methods.
        '''
        
        self._trades = trades
        self._quotes = quotes

        # Make sure data is in the right format
#         if ( data == None ) or ( data.getPrice == None ) or ( data.getTimestamp == None ) or ( data.getN == None ):
#             raise Exception( "Your data object must implement getPrice(i), getTimestamp(i), and getN() methods" ) 
    
    def getTradeDates(self):
        return [date for date in set(i[0] for i in self._trades)]
    
    def getQuotesDates(self):
        return [date for date in set(i[0] for i in self._quotes)]
    
    #part 2.a
    #how many days in the data for a ticker
    def getSampleLength(self):
        return len(self.getTradeDates())
  
    #part 2.b
    def getNumofTrades(self):
        return len(self._trades)
  
    def getNumofQuotes(self):
        return len(self._quotes)
     
    def getTradestoQuotes(self):
        if not self.getNumofQuotes():
            return -1
        return self.getNumofTrades() / self.getNumofQuotes()
# #     
#     #part 2.c
#     
    def getTradeReturns(self, seconds):
        return getXSecTradeReturns(self._trades, seconds)
    
    def getMidQuoteReturns(self, seconds):
        return getXSecMidQuoteReturns(self._quotes, seconds)
    
    
    # Mean Returns
    # Check annualization
    def _getMeanReturns(self, data):
        return np.mean( data ) 
    
    def getTradeMeanReturns(self, seconds):
        return self._getMeanReturns(self.getTradeReturns(seconds)) * ( 252 / len(self.getTradeDates()) )

    def getQuoteMeanReturns(self, seconds):
        return self._getMeanReturns(self.getMidQuoteReturns(seconds)) * ( 252 / len(self.getQuotesDates()) )
    
    # Std Deviations
    # Check annualization
    def _getStdReturns(self, data):
        return np.std( data ) 
    
    def getTradeStdReturns(self, seconds):
        return self._getStdReturns(self.getTradeReturns(seconds)) * np.sqrt(( 252 / len(self.getTradeDates())))

    def getMidQuoteStdReturns(self, seconds):
        return self._getStdReturns(self.getMidQuoteReturns(seconds)) * np.sqrt(( 252 / len(self.getQuotesDates())))
     
     
### HERE
    def getTradeMedianAbsDev(self, seconds):
        return median_absolute_deviation( self.getTradeReturns(seconds) ) * ( 252 / len(self.getTradeDates()))
    
    def getMidQuoteMedianAbsDev(self, seconds):
        return median_absolute_deviation( self.getMidQuoteReturns(seconds) ) * ( 252 / len(self.getQuotesDates()))
     
    def getTradeSkew(self, seconds):
        return skew( self.getTradeReturns(seconds) ) * ( 252 / len(self.getTradeDates()))
    
    def getMidQuoteSkew(self, seconds):
        return skew( self.getMidQuoteReturns(seconds) ) * ( 252 / len(self.getQuotesDates()))
     
    def getTradeKurtosis(self, seconds):
        return kurtosis( self.getTradeReturns( seconds ) ) * ( 252 / len(self.getTradeDates()))
    
    def getMidQuoteKurtosis(self, seconds):
        return kurtosis( self.getMidQuoteReturns(seconds) ) * ( 252 / len(self.getQuotesDates()))
    
    def get10largestTrade(self, seconds):
        return heapq.nlargest(10, self.getTradeReturns( seconds ) )
     
    def get10largestMidQuote(self, seconds):
        return heapq.nlargest(10, self.getMidQuoteReturns(seconds) )
    
    def get10smallestTrade(self, seconds):
        return heapq.nsmallest(10, self.getTradeReturns( seconds ) )
    
    def get10smallestMidQuote(self, seconds):
        return heapq.nsmallest(10, self.getMidQuoteReturns(seconds ) )
#     

#     
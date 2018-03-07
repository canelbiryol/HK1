'''
Created on Mar 6, 2018

@author: canelbiryol
'''
import time
import pandas as pd
import numpy as np

from adjustAndClean.TAQAdjust import TAQAdjust
from adjustAndClean.TAQCleaner import TAQCleaner
from adjustAndClean.StackData import StackData

from partB.TAQStats import TAQStats

if __name__ == '__main__':
    #baseDir = "/Users/canelbiryol/R"
    baseDir = "/Users/canelbiryol/Documents/SampleTAQ"
    startDate = "20070620"
    endDate = "20070621"
    #ticker = 'GOOG'
    ticker = 'IBM'
    startTime = time.time()
    print("* Started at {:s}".format(time.ctime()))
    
    # Get S&P tickers
#     s_p500 = '/Users/canelbiryol/s_p500.xlsx'
#     s_p500xls = pd.read_excel(open(s_p500,'rb'), sheet_name='WRDS')
#     s_ptickers = np.unique((np.array(s_p500xls['Ticker Symbol'])).astype(str))
#     s_ptickers = s_ptickers[:-1]
#     print("* Read S&P file at {:02f} secs".format(time.time() - startTime))

    
    # Stack all data for the ticker
    stack = StackData(baseDir, startDate, endDate, ticker)
    stack.addTrades()
    stack.addQuotes()
    print("* Stacked at {:02f} secs".format(time.time() - startTime))
    
    # Get results
    quotes = stack.getStackedQuotes()
    trades = stack.getStackedTrades()
    
    # Adjust the stacked data
#     adjuster = TAQAdjust( quotes, trades, ticker, s_p500 )
#     adjuster.adjustQuote()
#     adjuster.adjustTrade()
#     print("* Adjusted at {:02f} secs".format(time.time() - startTime))
#     
#     # Get results
#     quotes = adjuster.getStackedQuotes()
#     trades = adjuster.getStackedTrades()
#      
#     # Clean the adjusted data
#     cleaner = TAQCleaner(quotes, trades, k=45, gamma = 0.02)
#     quotes = np.delete(quotes, cleaner.cleanQuotesIndices(), axis = 0)
#     trades = np.delete(trades, cleaner.cleanTradesIndices(), axis = 0)
#     print("* Cleaned at {:02f} secs".format(time.time() - startTime))
    
    # Calculate Stats for Adjusted and Clean Data
    taqstats = TAQStats(trades, quotes)
    print("---------- Stats ----------------")
    print("N Sample : {:d}".format(taqstats.getSampleLength()))
    print("N Trades : {:d}".format(taqstats.getNumofTrades()))
    print("N Quotes : {:d}".format(taqstats.getNumofQuotes()))
    print("Trades / Quotes : {:f}".format(taqstats.getTradestoQuotes()))
    
    seconds = 600
    print("---------- Trade Returns ----------------")
    print("Mean: {:E}".format(taqstats.getTradeMeanReturns(seconds)))
    print("STD: {:E}".format(taqstats.getTradeStdReturns(seconds)))
    print("Median Abs Dev: {:E}".format(taqstats.getTradeMedianAbsDev(seconds)))
    print("Skew: {:E}".format(taqstats.getTradeSkew(seconds)))
    print("Kurtosis: {:E}".format(taqstats.getTradeKurtosis(seconds)))
    print("10 largest: " + ', '.join(str(x) for x in taqstats.get10largestTrade(seconds)))
    print("10 smallest: " + ', '.join(str(x) for x in taqstats.get10smallestTrade(seconds)))
   
    
    seconds = 600
    print("---------- Mid-Quote Returns ----------------")
    print("Mean: {:E}".format(taqstats.getQuoteMeanReturns(seconds)))
    print("STD: {:E}".format(taqstats.getMidQuoteStdReturns(seconds)))
    print("Median Abs Dev: {:E}".format(taqstats.getMidQuoteMedianAbsDev(seconds)))
    print("Skew: {:E}".format(taqstats.getMidQuoteSkew(seconds)))
    print("Kurtosis: {:E}".format(taqstats.getMidQuoteKurtosis(seconds)))
    print("10 largest: " + ', '.join(str(x) for x in taqstats.get10largestMidQuote(seconds)))
    print("10 smallest: " + ', '.join(str(x) for x in taqstats.get10smallestMidQuote(seconds)))
    
    # run your code
    endTime = time.time()
    print("* Ended at {:02f} secs".format((endTime - startTime)))
    
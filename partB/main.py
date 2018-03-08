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
from matplotlib import pyplot as plt

from partB.TAQStats import TAQStats

def printStats(trades, quotes, seconds):
    taqstats = TAQStats(trades, quotes)
    print("N Sample Days: {:d}".format(taqstats.getSampleLength()))
    print("N Trades : {:d}".format(taqstats.getNumofTrades()))
    print("N Quotes : {:d}".format(taqstats.getNumofQuotes()))
    print("Trades / Quotes : {:f}".format(taqstats.getTradestoQuotes()))
     
    print("---------------- Trade Returns ----------------")
    print("Mean Return: {:E}".format(taqstats.getTradeMeanReturns(seconds)))
    print("Median Return: {:E}".format(taqstats.getTradeMedianReturns(seconds)))
    print("STD of Return: {:E}".format(taqstats.getTradeStdReturns(seconds)))
    print("Median Abs Dev: {:E}".format(taqstats.getTradeMedianAbsDev(seconds)))
    print("Skew: {:E}".format(taqstats.getTradeSkew(seconds)))
    print("Kurtosis: {:E}".format(taqstats.getTradeKurtosis(seconds)))
    print("10 largest: " + ', '.join(str(x) for x in taqstats.get10largestTrade(seconds)))
    print("10 smallest: " + ', '.join(str(x) for x in taqstats.get10smallestTrade(seconds)))
    
 
    print("---------------- Mid-Quote Returns ----------------")
    print("Mean Return: {:E}".format(taqstats.getQuoteMeanReturns(seconds)))
    print("Median Return: {:E}".format(taqstats.getQuoteMedianReturns(seconds)))
    print("STD of Return: {:E}".format(taqstats.getMidQuoteStdReturns(seconds)))
    print("Median Abs Dev: {:E}".format(taqstats.getMidQuoteMedianAbsDev(seconds)))
    print("Skew: {:E}".format(taqstats.getMidQuoteSkew(seconds)))
    print("Kurtosis: {:E}".format(taqstats.getMidQuoteKurtosis(seconds)))
    print("10 Largest Returns: " + ', '.join(str(x) for x in taqstats.get10largestMidQuote(seconds)))
    print("10 Smallest Returns: " + ', '.join(str(x) for x in taqstats.get10smallestMidQuote(seconds)))
    
    return taqstats

def plotReturns(taqstats, seconds, title, outputFile):
    fig = plt.figure()
    plt.plot(taqstats.getTradeReturnsTimestamps(seconds), taqstats.getTradeReturns(seconds), label = 'Trades' )
    plt.plot(taqstats.getMidQuoteReturnsTimestamps(seconds), taqstats.getMidQuoteReturns(seconds), label = 'Mid-Quotes' ) 
    plt.title(title)
    plt.legend(bbox_to_anchor=(1.05, 1), loc="upper right", borderaxespad=0.)
    plt.show(block=False)
    fig.savefig(outputFile)
    
    
    
if __name__ == '__main__':
    #baseDir = "/Users/canelbiryol/R"
    baseDir = "/Users/canelbiryol/Documents/SampleTAQ"
    startDate = "20070620"
    endDate = "20070621"
    #ticker = 'GOOG'
    ticker = 'IBM'
    seconds = 600
    k = 45
    gamma = 0.02
    
    
    startTime = time.time()
    print("* Started at {:s}".format(time.ctime()))
    
    #Get S&P tickers
    s_p500 = '/Users/canelbiryol/s_p500.xlsx'
    s_p500xls = pd.read_excel(open(s_p500,'rb'), sheet_name='WRDS')
    s_ptickers = np.unique((np.array(s_p500xls['Ticker Symbol'])).astype(str))
    s_ptickers = s_ptickers[:-1]
    print("* Read S&P file at {:02f} secs".format(time.time() - startTime))

    
    ### Stack Data
    stack = StackData(baseDir, startDate, endDate, ticker)
    stack.addTrades()
    stack.addQuotes()
    print("* Stacked at {:02f} secs".format(time.time() - startTime))
    
    # Get results
    quotes = stack.getStackedQuotes()
    trades = stack.getStackedTrades()
    
    ### Adjust Data
    adjuster = TAQAdjust( quotes, trades, ticker, s_p500 )    
    adjuster.adjustQuote()
    adjuster.adjustTrade()
    print("* Adjusted at {:02f} secs".format(time.time() - startTime))
    
    # Get results
    quotes = adjuster.getStackedQuotes()
    trades = adjuster.getStackedTrades()
    print("----------------------------------------------------------------------")
    print("---------------- Stats for Adjusted but Unclean Data ------------------")
    print("----------------------------------------------------------------------")
    taqstats = printStats(trades, quotes, seconds)
    
    # Plot
    title = str(seconds) + ' seconds Trade and Mid-Quote Returns for ' + ticker + '\nwith the Adjusted Data'
    outputFile = "/Users/canelbiryol/Figs/" + ticker + "_" + str(seconds) + "sec_adjusted.png"
    plotReturns(taqstats, seconds, title, outputFile)
    
    ### Clean Data
    cleaner = TAQCleaner(quotes, trades, k, gamma )
    print("* Cleaned at {:02f} secs".format(time.time() - startTime))
    
    # Get results
    quotes = np.delete(quotes, cleaner.cleanQuotesIndices(), axis = 0)
    trades = np.delete(trades, cleaner.cleanTradesIndices(), axis = 0)
    print("----------------------------------------------------------------------")
    print("---------------- Stats for Adjusted and Clean Data ----------------")
    print("----------------------------------------------------------------------")
    taqstats = printStats(trades, quotes, seconds)
    
    # Plot
    title = '{:d} seconds Trade and Mid-Quote Returns for {:s}\nwith the Adjusted and Cleaned Data. ( k: {:d}, gamma: {:f} )'.format(
            seconds,
            ticker,
            k,
            gamma
        )
    
    #str(seconds) + ' seconds Trade and Mid-Quote Returns for ' + ticker + '\nwith the Adjusted and Cleaned Data' + '\nk: ' + str(k) + ', gamma: ' + str(gamma)
    outputFile = "/Users/canelbiryol/Figs/" + ticker + "_" + str(seconds) + "sec_adjusted_clean.png"
    plotReturns(taqstats, seconds, title, outputFile)
     
    # run your code
    endTime = time.time()
    print("* Ended at {:02f} secs".format((endTime - startTime)))
    
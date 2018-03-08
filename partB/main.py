'''
Created on Mar 6, 2018

@author: canelbiryol
'''
import time
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from datetime import datetime

from adjustAndClean.TAQAdjust import TAQAdjust
from adjustAndClean.TAQCleaner import TAQCleaner
from adjustAndClean.StackData import StackData

from partB.TAQStats import TAQStats

def printStats(trades, quotes, seconds):
    taqstats = TAQStats(trades, quotes, seconds)
    print("N Sample Days: {:d}".format(taqstats.getSampleLength()))
    print("N Trades : {:d}".format(taqstats.getNumofTrades()))
    print("N Quotes : {:d}".format(taqstats.getNumofQuotes()))
    print("Trades / Quotes : {:f}".format(taqstats.getTradestoQuotes()))
     
    print("---------------- Trade Returns ----------------")
    print("Mean Return: {:E}".format(taqstats.getTradeMeanReturns()))
    print("Median Return: {:E}".format(taqstats.getTradeMedianReturns()))
    print("STD of Return: {:E}".format(taqstats.getTradeStdReturns()))
    print("Median Abs Dev: {:E}".format(taqstats.getTradeMedianAbsDev()))
    print("Skew: {:E}".format(taqstats.getTradeSkew()))
    print("Kurtosis: {:E}".format(taqstats.getTradeKurtosis()))
    print("10 largest: " + ', '.join(str(x) for x in taqstats.get10largestTrade()))
    print("10 smallest: " + ', '.join(str(x) for x in taqstats.get10smallestTrade()))
    
 
    print("---------------- Mid-Quote Returns ----------------")
    print("Mean Return: {:E}".format(taqstats.getQuoteMeanReturns()))
    print("Median Return: {:E}".format(taqstats.getQuoteMedianReturns()))
    print("STD of Return: {:E}".format(taqstats.getMidQuoteStdReturns()))
    print("Median Abs Dev: {:E}".format(taqstats.getMidQuoteMedianAbsDev()))
    print("Skew: {:E}".format(taqstats.getMidQuoteSkew()))
    print("Kurtosis: {:E}".format(taqstats.getMidQuoteKurtosis()))
    print("10 Largest Returns: " + ', '.join(str(x) for x in taqstats.get10largestMidQuote()))
    print("10 Smallest Returns: " + ', '.join(str(x) for x in taqstats.get10smallestMidQuote()))
    
    return taqstats

def plotReturns(taqstats, title, outputFile):
    fig = plt.figure()
#     ax=plt.gca()
#     xfmt = md.DateFormatter('%Y-%m-%d %H:%M:%S')
#     ax.xaxis.set_major_formatter(xfmt)
#     x = [datetime.fromtimestamp(element) for element in taqstats.getTradeReturnsTimestamps()]
#     x = taqstats.getTradeReturnsTimestamps()
    plt.plot(taqstats.getTradeReturns(), label = 'Trades')
#     x = [datetime.fromtimestamp(element) for element in taqstats.getMidQuoteReturnsTimestamps()]
#     x = taqstats.getMidQuoteReturnsTimestamps()
    plt.plot(taqstats.getMidQuoteReturns(), label = 'Mid-Quotes') 
    plt.gcf().autofmt_xdate()
    plt.title(title)
    plt.legend(bbox_to_anchor=(1.05, 1), loc="upper right", borderaxespad=0.)
    plt.show(block=False)
    fig.savefig(outputFile)
    
    
    
if __name__ == '__main__':
    baseDir = "/Users/canelbiryol/R"
    #baseDir = "/Users/canelbiryol/Documents/SampleTAQ"
    startDate = "20070620"
    endDate = "20070921"
    ticker = 'MSFT'
    #ticker = 'IBM'
    seconds = 60
    k = 45
    gamma = 0.02
    
    print(str(ticker) + ", " + str(seconds) + " seconds, k: " + str(k) + ", gamma: " + str(gamma))
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
    
    # Get results
    quotes = stack.getStackedQuotes()
    trades = stack.getStackedTrades()
    
    print("* Stacked at {:02f} secs".format(time.time() - startTime))
    
    ### Adjust Data
    adjuster = TAQAdjust( quotes, trades, ticker, s_p500 )    
    adjuster.adjustQuote()
    adjuster.adjustTrade()
    
    # Get results
    quotes = adjuster.getStackedQuotes()
    trades = adjuster.getStackedTrades()
    
    print("* Adjusted at {:02f} secs".format(time.time() - startTime))
    
    print("----------------------------------------------------------------------")
    print("---------------- Stats for Adjusted but Unclean Data ------------------")
    print("----------------------------------------------------------------------")
    taqstats = printStats(trades, quotes, seconds)
    
    # Plot Trade and Mid-Quote Returns
    title = str(seconds) + ' seconds Trade and Mid-Quote Returns for ' + ticker + '\nwith the Adjusted Data'
    outputFile = "/Users/canelbiryol/Figs/" + ticker + "_" + str(seconds) + "sec_adjusted.png"
    plotReturns(taqstats, title, outputFile)
    
    ### Clean Data
    cleaner = TAQCleaner(quotes, trades, k, gamma )
    
    
    # Get results
    quotes = np.delete(quotes, cleaner.cleanQuotesIndices(), axis = 0)
    trades = np.delete(trades, cleaner.cleanTradesIndices(), axis = 0)
    
    print("* Cleaned at {:02f} secs".format(time.time() - startTime))
    
    print("----------------------------------------------------------------------")
    print("---------------- Stats for Adjusted and Clean Data ----------------")
    print("----------------------------------------------------------------------")
    taqstats = printStats(trades, quotes, seconds)
    
    # Plot Trade and Mid-Quote Returns
    title = '{:d} seconds Trade and Mid-Quote Returns for {:s}\nwith the Adjusted and Cleaned Data. ( k: {:d}, gamma: {:f} )'.format(
            seconds,
            ticker,
            k,
            gamma
        )
    
    outputFile = "/Users/canelbiryol/Figs/" + ticker + "_" + str(seconds) + "sec_adjusted_clean.png"
    plotReturns(taqstats, title, outputFile)
     
    # run your code
    endTime = time.time()
    print("* Ended at {:02f} secs".format((endTime - startTime)))
    
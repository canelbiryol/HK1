'''
Created on Mar 27, 2018

@author: Michael
'''
import numpy as np
import pandas as pd
from adjustAndClean.TAQAdjust import TAQAdjust
from adjustAndClean.TAQCleaner import TAQCleaner
from adjustAndClean.StackData import StackData
import time
import os
        
"""
"""

print('Initializing.')

""" TO SPECIFY """
baseDir = '/Users/Michael/Documents/TAQ/R'

""" TO SPECIFY """
filepathcln = '/Users/Michael/Documents/TAQ/R/cleaned'

""" TO SPECIFY """
s_p500 = '/Users/Michael/eclipse-workspace/Homework_1/s_p500.xlsx'

# S&P500 tickers
s_p500xls = pd.read_excel(open(s_p500,'rb'), sheet_name='WRDS')
s_ptickers = np.unique((np.array(s_p500xls['Ticker Symbol'])).astype(str))
list_tickers = s_ptickers[:-1]

dates = os.listdir(baseDir + '/quotes/')
D = len(dates)
#Add dummy date
dates.append('20070921')
for i in range(D):
    startDate = dates[i]
    endDate = dates[i+1]

    for ticker in list_tickers:
        # Stack everything
        start = time.time()
        print("j")
        stack = StackData(baseDir, startDate, endDate, ticker)
        print('k')
        stack.addQuotes()
        stack.addTrades()
        end = time.time()
        print(end - start)
        print('Finished stacking', ticker)
                
        # Get results
        quotes = stack.getStackedQuotes()
        trades = stack.getStackedTrades()
        print('Got results', ticker)
                
        # Adjust
        adjuster = TAQAdjust( quotes, trades, ticker, s_p500 )
        adjuster.adjustQuote()
        adjuster.adjustTrade()
        print('Adjusted', ticker)
                
        # Clean
        cleaner = TAQCleaner(quotes, trades, ticker)
        quotes = np.delete(quotes, cleaner.cleanQuotesIndices(), axis = 0)
        trades = np.delete(trades, cleaner.cleanTradesIndices(), axis = 0)
        print('Cleaned', ticker)
    
        cleaner.storeCleanedQuotes(filepathcln)
        cleaner.storeCleanedTrades(filepathcln)
        print('Stored cleaned', ticker)
        
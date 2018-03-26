import numpy as np
import pandas as pd
from adjustAndClean.TAQAdjust import TAQAdjust
from adjustAndClean.TAQCleaner import TAQCleaner
from adjustAndClean.StackData import StackData
import time
        
"""
"""

print('Initializing.')
# FIRST: Take S&P500 tickers
""" TO SPECIFY """
s_p500 = '/media/louis/DATA/documents/cours/NYU/SPRING_18/ATQS/HK1/s_p500.xlsx'

s_p500xls = pd.read_excel(open(s_p500,'rb'), sheet_name='WRDS')
s_ptickers = np.unique((np.array(s_p500xls['Ticker Symbol'])).astype(str))
s_ptickers = s_ptickers[:-1]
print(s_ptickers)

""" TO SPECIFY """
baseDir = '/media/louis/DATA/Courant_dataset_matlab/R'

""" TO SPECIFY """
filepathcln = '/media/louis/DATA/cleandata/'

""" TO SPECIFY """
tickers_todo = '/media/louis/DATA/documents/cours/NYU/SPRING_18/ATQS/HK1/split_adjust_clean.xlsx'

list_tickers_xls = pd.read_excel(open(tickers_todo,'rb'), sheet_name='Canel')
list_tickers = np.unique((np.array(list_tickers_xls['Ticker Symbol'])).astype(str))
list_tickers = list_tickers[:-1]
print(list_tickers)

startDate = '20070620'
endDate = '20070921'

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
import numpy as np
import pandas as pd
from adjustAndClean.TAQAdjust import TAQAdjust
from adjustAndClean.TAQCleaner import TAQCleaner
from adjustAndClean.StackData import StackData
        
"""
"""

print('Initializing.')
# FIRST: Take S&P500 tickers
s_p500 = '/media/louis/DATA/documents/cours/NYU/SPRING_18/ATQS/HK1/s_p500.xlsx'
s_p500xls = pd.read_excel(open(s_p500,'rb'), sheet_name='WRDS')
s_ptickers = np.unique((np.array(s_p500xls['Ticker Symbol'])).astype(str))
s_ptickers = s_ptickers[:-1]
baseDir = '/media/louis/DATA/Courant_dataset_matlab/R'
filepathcln = '/media/louis/DATA/cleandata/'
startDate = '20070620'
endDate = '20070921'
ticker1 = 'AAPL'

# Stack everything
print("j")
stack = StackData(baseDir, startDate, endDate, ticker1)
print('k')
stack.addQuotes()
stack.addTrades()
print('Finished stacking AAPL')
            
# Get results
quotes = stack.getStackedQuotes()
trades = stack.getStackedTrades()
print('Got results AAPL')
            
# Adjust
adjuster = TAQAdjust( quotes, trades, s_p500 )
adjuster.adjustQuote()
adjuster.adjustTrade()
print('Adjusted AAPL')
            
# Clean
cleaner = TAQCleaner(quotes, trades)
quotes = np.delete(quotes, cleaner.cleanQuotesIndices(), axis = 0)
trades = np.delete(trades, cleaner.cleanTradesIndices(), axis = 0)
print('Cleaned AAPL')

cleaner.storeCleanedQuotes(filepathcln)
cleaner.storeCleanedTrades(filepathcln)
print('Stored clean AAPL')

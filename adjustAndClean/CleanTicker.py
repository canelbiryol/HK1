import numpy as np
import pandas as pd
from adjustAndClean.TAQAdjust import TAQAdjust
from adjustAndClean.TAQCleaner import TAQCleaner
from adjustAndClean.StackData import StackData
import time
from _operator import index
        
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
endDate = '20070621'
ticker1 = 'MSFT'

# Stack everything
start = time.time()
print("j")
stack = StackData(baseDir, startDate, endDate, ticker1)
print('k')
stack.addQuotes()
stack.addTrades()
end = time.time()
print(end - start)
print('Finished stacking MSFT')
            
# Get results
quotes = stack.getStackedQuotes()
trades = stack.getStackedTrades()
print('Got results MSFT')
            
# Adjust
adjuster = TAQAdjust( quotes, trades, ticker1, s_p500 )
adjuster.adjustQuote()
adjuster.adjustTrade()
print('Adjusted MSFT')
            
# Clean
cleaner = TAQCleaner(quotes, trades, ticker1, kT=45, gammaT=0.0002, kQ=45, gammaQ=0.0002)
indextrades = cleaner.cleanTradesIndices()
print((len(indextrades) - np.count_nonzero(indextrades))/len(indextrades))
indexquotes = cleaner.cleanQuotesIndices()
print((len(indexquotes) - np.count_nonzero(indexquotes))/len(indexquotes))
quotes = quotes[indexquotes==True,:]
trades = trades[indextrades==True,:]
print('Cleaned MSFT')

cleaner.storeCleanedQuotes(filepathcln)
cleaner.storeCleanedTrades(filepathcln)
print('Stored clean MSFT')

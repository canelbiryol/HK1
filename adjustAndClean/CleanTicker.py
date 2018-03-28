import numpy as np
import pandas as pd
from adjustAndClean.TAQAdjust import TAQAdjust
from adjustAndClean.TAQCleaner import TAQCleaner
from adjustAndClean.StackData import StackData
from adjustAndClean.AdjustingHashmap import AdjustingHashmap
import time

"""
Stack, adjust, clean and store in binary format at specified location the data
for one specified ticker and time frame.
"""

print('Initializing')

# S&P500 tickers and user's parameters
s_p500 = '/media/louis/DATA/documents/cours/NYU/SPRING_18/ATQS/HK1/s_p500.xlsx'
s_p500xls = pd.read_excel(open(s_p500,'rb'), sheet_name='WRDS')
s_ptickers = np.unique((np.array(s_p500xls['Ticker Symbol'])).astype(str))
s_ptickers = s_ptickers[:-1]
baseDir = '/media/louis/DATA/Courant_dataset_matlab/R'
filepathcln = '/media/louis/DATA/cleandata/'
startDate = '20070620'
endDate = '20070621'
ticker = 'MSFT'

# Multipliers map
print("\nStarted building multipliers table {:s}".format(ticker))
start = time.time()
multmap = AdjustingHashmap(s_p500)
end = time.time()
print('Finished building multipliers table {:s} at {:.1f}s'.format(ticker, (end - start)))

# Stack everything
stack = StackData(baseDir, startDate, endDate, ticker)
stack.addQuotes()
stack.addTrades()
end = time.time()
print('Finished stacking {:s} at {:.1f}s'.format(ticker, (end - start)))
            
# Get results
quotes = stack.getStackedQuotes()
trades = stack.getStackedTrades()
end = time.time()
print('Got results {:s} at {:.1f}s'.format(ticker, (end - start)))

# Adjust
adjuster = TAQAdjust( quotes, trades, ticker, multmap)
adjuster.adjustQuote()
adjuster.adjustTrade()
end = time.time()
print('Adjusted {:s} at {:.1f}s'.format(ticker, (end - start)))
            
# Clean
cleaner = TAQCleaner(quotes, trades, ticker)
indextrades = cleaner.cleanTradesIndices()
indexquotes = cleaner.cleanQuotesIndices()
quotes = quotes[indexquotes==True,:]
trades = trades[indextrades==True,:]
print((len(indextrades) - np.count_nonzero(indextrades))/len(indextrades))
print((len(indexquotes) - np.count_nonzero(indexquotes))/len(indexquotes))
end = time.time()
print('Cleaned {:s} at {:.1f}s'.format(ticker, (end - start)))
             
cleaner.storeCleanedQuotes(filepathcln)
cleaner.storeCleanedTrades(filepathcln)
end = time.time()
print('Stored cleaned {:s} at {:.1f}s'.format(ticker, (end - start)))


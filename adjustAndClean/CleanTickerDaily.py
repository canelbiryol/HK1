import numpy as np
import pandas as pd
from adjustAndClean.TAQAdjust import TAQAdjust
from adjustAndClean.TAQCleaner import TAQCleaner
from adjustAndClean.StackData import StackData
from adjustAndClean.AdjustingHashmap import AdjustingHashmap
import time
import os

"""
Stack, adjust, clean and store in binary format at specified location the data
for specified list of tickers and time frame.
"""

print('Initializing')

""" TO SPECIFY """
s_p500 = '/media/louis/DATA/documents/cours/NYU/SPRING_18/ATQS/HK1/s_p500.xlsx'

# S&P tickers
s_p500xls = pd.read_excel(open(s_p500,'rb'), sheet_name='WRDS')
s_ptickers = np.unique((np.array(s_p500xls['Ticker Symbol'])).astype(str))
s_ptickers = s_ptickers[:-1]

""" TO SPECIFY """
baseDir = '/media/louis/DATA/Courant_dataset_matlab/R'
""" TO SPECIFY """
filepathcln = '/media/louis/DATA/cleandata/'
""" TO SPECIFY """
tickers_todo = '/media/louis/DATA/documents/cours/NYU/SPRING_18/ATQS/HK1/split_adjust_clean.xlsx'
""" TO SPECIFY (your name!) """
list_tickers_xls = pd.read_excel(open(tickers_todo,'rb'), sheet_name='Louis')

# List of tickers todo
list_tickers = np.unique((np.array(list_tickers_xls['Ticker Symbol'])).astype(str))
list_tickers = list_tickers[:-1]
""" IF YOU DON'T WANT EVERYTHING, uncomment this line """
list_tickers = s_ptickers
print(list_tickers)

# Timeframe
startDate = '20070620'
endDate = '20070921'
dates = os.listdir(baseDir + '/quotes/')
dates.append('20070930') # dummy date for the end
dates = np.sort(dates)
print(dates)

# Multipliers table
print("\nStarted building multipliers table")
start = time.time()
multmap = AdjustingHashmap(s_p500)
end = time.time()
print('Finished building multipliers table at {:.1f}s'.format((end - start)))

i = 0
errored = []
D = len(dates)
start = time.time()
for i in range(D):
    startDate = dates[i]
    endDate = dates[i+1]

    end = time.time()
    print("Start of day {:d} at {:.1f}s".format(i, (end - start)))
    
    j = 0
    for ticker in list_tickers:
        try:
            print("\n\nStarted processing {:d} of {:d}: {:s}".format(j, len(list_tickers), ticker))
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
            adjuster = TAQAdjust( quotes, trades, ticker, multmap )
            adjuster.adjustQuote()
            adjuster.adjustTrade()
            end = time.time()
            print('Adjusted {:s} at {:.1f}s'.format(ticker, (end - start)))
                         
            # Clean
            cleaner = TAQCleaner(quotes, trades, ticker)
            quotes = quotes[cleaner.cleanQuotesIndices()==True,:]
            trades = trades[cleaner.cleanTradesIndices()==True,:]
            end = time.time()
            print('Cleaned {:s} at {:.1f}s'.format(ticker, (end - start)))
             
            cleaner.storeCleanedQuotes(filepathcln)
            cleaner.storeCleanedTrades(filepathcln)
            end = time.time()
            print('Stored cleaned {:s} at {:.1f}s'.format(ticker, (end - start)))

            j = j+1
        except Exception as e:
            errored.append(ticker)
            print("!!!! Failed processing ticker: {:s}".format(ticker))
            print(e)
       
    end = time.time()
    print('Done with day {:d} at {:.1f}s'.format(i, (end - start)))
              
print("!!!! Failed processing following tickers: {:s}".format(",".join(errored)))
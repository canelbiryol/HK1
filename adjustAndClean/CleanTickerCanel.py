import numpy as np
import pandas as pd
from adjustAndClean.TAQAdjust import TAQAdjust
from adjustAndClean.TAQCleaner import TAQCleaner
from adjustAndClean.StackData import StackData
import time
import os
# from adjustAndClean.AdjAndCleanDaily import startDate
        
"""
"""

print('Initializing.')
# FIRST: Take S&P500 tickers
""" TO SPECIFY """
s_p500 = "/Users/canelbiryol/HK1/s_p500.xlsx"

s_p500xls = pd.read_excel(open(s_p500,'rb'), sheet_name='WRDS')
s_ptickers = np.unique((np.array(s_p500xls['Ticker Symbol'])).astype(str))
s_ptickers = s_ptickers[:-1]
print(s_ptickers)

""" TO SPECIFY """
baseDir = "/Users/canelbiryol/R"

""" TO SPECIFY """
filepathcln = "/Users/canelbiryol/Data/CleanDailyData"

""" TO SPECIFY """
tickers_todo = '/Users/canelbiryol/HK1/split_adjust_clean.xlsx'

list_tickers_xls = pd.read_excel(open(tickers_todo,'rb'), sheet_name='Canel')
list_tickers = np.unique((np.array(list_tickers_xls['Ticker Symbol'])).astype(str))
list_tickers = list_tickers[:-1]
#print(list_tickers)

# startDate = '20070620'
# endDate = '20070921'

i = 0
j = 0
errored = []

dates = os.listdir(baseDir + '/quotes/')
D = len(dates)
dates.remove('.DS_Store')
dates.sort()
print(dates)

for i in range(D):
    startDate = dates[i]
    endDate = dates[i+1]
    j = 0
    
    print(startDate + " - " + endDate)
    # print(dates)
    
    for ticker in list_tickers:
        try:
            j += 1
#             if os.path.exists(os.path.join(filepathcln, 'quotes', startDate, ticker + "_quotes.binRQ")):
#                 continue
            
            print("\n\nStarted processing {:d} of {:d}: {:s}".format(j, len(list_tickers), ticker))
            # Stack everything
            start = time.time()
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
            adjuster = TAQAdjust( quotes, trades, ticker, s_p500 )
            adjuster.adjustQuote()
            adjuster.adjustTrade()
            end = time.time()
            print('Adjusted {:s} at {:.1f}s'.format(ticker, (end - start)))
                         
            # Clean
            cleaner = TAQCleaner(quotes, trades, ticker)
            quotes = np.delete(quotes, cleaner.cleanQuotesIndices(), axis = 0)
            trades = np.delete(trades, cleaner.cleanTradesIndices(), axis = 0)
            end = time.time()
            print('Cleaned {:s} at {:.1f}s'.format(ticker, (end - start)))
             
            cleaner.storeCleanedQuotes(filepathcln)
            cleaner.storeCleanedTrades(filepathcln)
            end = time.time()
            print('Stored cleaned {:s} at {:.1f}s'.format(ticker, (end - start)))
        except Exception as e:
            errored.append(ticker)
            print("!!!! Failed processing ticker: {:s}".format(ticker))
            print(e)
             
        
    
print("!!!! Failed processing following tickers: {:s}".format(",".join(errored)))
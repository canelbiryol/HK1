'''
Created on Mar 9, 2018

@author: Michael
'''
import numpy as np
import pandas as pd
from adjustAndClean.TAQAdjust import TAQAdjust
from adjustAndClean.TAQCleaner import TAQCleaner
from adjustAndClean.StackData import StackData
from partB.xMinuteReturn import getXSecMidQuoteReturns
from partB.xMinuteReturn import getXSecTradeReturns
from Part_C.AutocorrelationPlotter import plotAutocorrelation
from Part_C.Ljung_Box import Ljung_Box
from statsmodels.tsa.stattools import adfuller

print('Initializing.')

    # FIRST: Take S&P500 tickers
s_p500 = '/Users/Michael/eclipse-workspace/Homework_1/s_p500.xlsx'
s_p500xls = pd.read_excel(open(s_p500,'rb'), sheet_name='WRDS')
s_ptickers = np.unique((np.array(s_p500xls['Ticker Symbol'])).astype(str))
s_ptickers = s_ptickers[:-1]
filepathcln = '/Users/Michael/Documents/TAQ/R/clean'

baseDir = '/Users/Michael/Documents/TAQ/R'
startDate = '20070620'
endDate = '20070921'
ticker1 = 'MSFT'
ticker2 = 'GOOG'

# Stack everything
stack = StackData(baseDir, startDate, endDate, ticker1)
stack.addTrades()
stack.addQuotes()
print('Finished stacking MSFT')
            
# Get results
quotes = stack.getStackedQuotes()
trades = stack.getStackedTrades()
print('Got results MSFT')
            
# Adjust
adjuster = TAQAdjust( quotes, trades, s_p500 )
adjuster.adjustQuote()
adjuster.adjustTrade()
print('Adjusted MSFT')
            
# Clean
cleaner = TAQCleaner(quotes, trades)
quotes = np.delete(quotes, cleaner.cleanQuotesIndices(), axis = 0)
trades = np.delete(trades, cleaner.cleanTradesIndices(), axis = 0)
print('Cleaned MSFT')

cleaner.storeCleanedQuotes(filepathcln)
cleaner.storeCleanedTrades(filepathcln)
print('Stored clean MSFT')


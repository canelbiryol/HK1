'''
Created on Mar 28, 2018

@author: canelbiryol
'''

import numpy as np
import pandas as pd
import json
import time
import os
import csv
import xlwt
import glob
import itertools
from adjustAndClean.StackData import StackData
from partB.xMinuteReturn import getXSecMidQuoteReturns
from impactModel.VWAP import VWAP
from impactModel.TickTest import TickTest

# compute 2-min mid-quote returns
def getXMinMidQuoteRet(data, delta):
    nRecs = len(data) 
    lastTs = int(data[0][1])
    lastMidQuote = (float(data[0][2]) + float(data[0][4])) / 2 
    
    midQuoteReturns = [] 
    timestamps = []
    for startI in range( 1, nRecs ):
        timestamp = int(data[startI][1])
        midQuote = (float(data[startI][2]) + float(data[startI][4])) / 2        
            
        # check this
        if timestamp > (lastTs + delta): 
            midQuoteReturns.append( (midQuote / lastMidQuote) - 1 )
            lastTs = lastTs + delta
            lastMidQuote = midQuote
            
    return midQuoteReturns

# compute STD of 2-min mid-quote returns
def getSTDXMinMidQuoteRet(data, delta):
    return np.std(getXMinMidQuoteRet(data, delta))

def getAvgN(data, n):
    return int(np.mean(data[0:n]))
# 
# def getN(data):
#     return len(data)

# compute total daily vol
def getTotalDailyVol(data):
    return int(np.sum([d[1] for d in data]))

# compute arrival price - average of first five mid-quote prices
def getArrivalPrice(data, n):
    midquotes = []

    for i in range(n):
        midquotes.append((data[i][2] + data[i][4]) / 2 )

    return sum(midquotes) / float(len(midquotes))

# compute terminal price - average of last 5 mid-quote prices
def getTerminalPrice(data, n):
    midquotes = []
    length = len(data)
    
    for i in range(n):
        midquotes.append((data[length - (i+1)][2] + data[length - (i + 1)][4]) / 2 )

    return sum(midquotes) / float(len(midquotes))

# compute volume weighted average price
def getVWAP(data, startTS, endTS):
    v = 0
    s = 0
    counter = 0
    for i in range( 0, len(data) ):
        if( float(data[i][1]) < startTS ):
            continue
        if( float(data[i][1]) >= endTS ):
            break
        
        counter = counter + 1
        v = v + ( data[i][2] * data[i][3] )
        s = s + data[i][3]
    
    return v / s

# compute volume weighted average price until 3:30 pm
def getVWAPuntil330(data):
    start930 = 19 * 60 * 60 * 1000 / 2
    end330 = 31 * 60 * 60 * 1000 / 2
    vwap = getVWAP( data, start930, end330 )
    return vwap

# compute volume weighted average price until 4:00 pm
def getVWAPuntil400(data, endTime):
    start930 = 19 * 60 * 60 * 1000 / 2
    end330 = 16 * 60 * 60 * 1000 
    vwap = getVWAP( data, start930, end330 )
    return vwap

# compute imbalance using the modified TickTest from impactModel
def getImbalance(data):
    start930 = 19 * 60 * 60 * 1000 / 2
    end330 = 16 * 60 * 60 * 1000
    
    tickTest = TickTest()
    classifications = tickTest.classifyAll( data, start930, end330 )
    
    imbalance = sum([ c[1] * c[2] for c in classifications])
    return imbalance
  
# export each matrices to csv file. Each rows are tickers and each columns are days
def exportToCSV(data, key):
    dw = data[key]
    
    with open(output + "/" + key + ".csv", "w") as f:
#         w = csv.writer( f )
#         days = list(dw.values())[0].keys()
#         print(days)
#         for key in dw.keys():
#             w.writerow([key] + [dw[key][day] for day in days])
        
        fields = ['ticker'] + [day for day in list(dw.values())[0].keys()]
        w = csv.DictWriter(f, fields )
        w.writeheader()
        for k in dw:
            w.writerow({field: dw[k].get(field) or k for field in fields})

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

output = '/Users/canelbiryol/Data/stats'

list_tickers_xls = pd.read_excel(open(tickers_todo,'rb'), sheet_name='Canel')
list_tickers = np.unique((np.array(s_p500xls['Ticker Symbol'])).astype(str))
list_tickers = list_tickers[:-1]

# startDate = '20070620'
# endDate = '20070921'

i = 0
j = 0
errored = []

dates = os.listdir(baseDir + '/quotes/')
D = len(dates)
#Add dummy date
dates.append('20070921')
dates.remove('.DS_Store')
dates.sort()


keys = ['arrival_price', 'imbalance', 'terminal_price', 'VWAPuntil330', 'VWAPuntil400', 'vol', 'imbalance_value', '2_minute_returns', 'std_2_min_returns']

stats = {}
for key in keys:
    stats[key] = {} 
        
        
for i in range(D):
    startDate = dates[i]
    endDate = dates[i+1]
    j = 0
    
    print(startDate + " - " + endDate)
     
    for ticker in list_tickers:
        try:

            if ticker == 'SYMC':
                break
            j += 1
            if not os.path.exists(os.path.join(filepathcln, 'quotes', startDate, ticker + "_quotes.binRQ")):
                continue
            stack = StackData(filepathcln, startDate, endDate, ticker)
            stack.addQuotes()
            stack.addTrades()
            
            quotes = stack.getStackedQuotes()
            trades = stack.getStackedTrades()

            for key in keys:
                if not ticker in stats[key]:
                    stats[key][ticker] = {} 
            
            stats['arrival_price'][ticker][startDate] = getArrivalPrice(quotes, 5)
            stats['imbalance'][ticker][startDate] = getImbalance(trades)      
            stats['terminal_price'][ticker][startDate] = getTerminalPrice(quotes, 5) 
            stats['VWAPuntil330'][ticker][startDate] = getVWAP(trades, 19 * 60 * 60 * 1000 / 2, 31 * 60 * 60 * 1000 / 2)
            stats['VWAPuntil400'][ticker][startDate] = getVWAP(trades, 19 * 60 * 60 * 1000 / 2, 16 * 60 * 60 * 1000)     
            stats['vol'][ticker][startDate] = getTotalDailyVol(trades)
            stats['imbalance_value'][ticker][startDate] = stats['imbalance'][ticker][startDate] * stats['VWAPuntil400'][ticker][startDate]
            stats['2_minute_returns'][ticker][startDate] = getXMinMidQuoteRet(quotes, 2 * 60 * 100)
            stats['std_2_min_returns'][ticker][startDate] = getSTDXMinMidQuoteRet(quotes, 2 * 60 * 100)
            
            # Remove later
     
    # Remove later
    #if i == 5:
    #zbreak     
        except Exception as e:
            print("!!!! Failed processing ticker: {:s}".format(ticker))
            print(e)

# print the results in console
print(json.dumps(stats, indent=2, sort_keys=True))
 
# Export to Excel
writer = pd.ExcelWriter(output + '/stats.xlsx')
for key in keys: 
    exportToCSV(stats, key)
    df = pd.read_csv(output + '/' + key + '.csv', index_col=0)
    df.to_excel(writer, sheet_name=key)
writer.save()    
#     
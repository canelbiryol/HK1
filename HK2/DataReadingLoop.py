'''
TODO: WRITE SPEC
'''

import numpy as np
import pandas as pd
import time
import os
import csv
from adjustAndClean.StackData import StackData
from impactModel.TickTest import TickTest


keys = ['arrival_price', 'imbalance', 'terminal_price', 'VWAPuntil330', 'VWAPuntil400', 'vol', 'imbalance_value', '2_minute_returns', 'std_2_min_returns']

times = {
    '9:30': 19 * 60 * 60 * 1000 / 2,
    '15:30': 31 * 60 * 60 * 1000 / 2,
    '16:00': 16 * 60 * 60 * 1000,
    '2min': 2 * 60 * 100
}

# print(int(times['16:00'] - times['9:30']) / times['2min'])
# compute 2-min mid-quote returns
def getXMinMidQuoteRet(data, delta):
    nRecs = len(data) 
    lastTs = int(data[0][1])
    lastMidQuote = (float(data[0][2]) + float(data[0][4])) / 2 
    
    midQuoteReturns = []
    for startI in range( 1, nRecs ):
        timestamp = int(data[startI][1])       
            
        # check this
        if timestamp > (lastTs + delta): 
            midQuote = (float(data[startI][2]) + float(data[startI][4])) / 2 
            midQuoteReturns.append( (midQuote / lastMidQuote) - 1 )
            lastTs = lastTs + delta
            lastMidQuote = midQuote
            
    return midQuoteReturns

# compute STD of 2-min mid-quote returns
def getSTDXMinMidQuoteRet(midQuoteReturns):
    return np.std(midQuoteReturns) * np.sqrt(252)

# compute total daily vol
def getTotalDailyVol(data):
    return int(np.sum([d[1] for d in data]))

# compute arrival price - average of first five mid-quote prices
def getArrivalPrice(data, n):
    midquotes = [None] * n

    for i in range(n):
        midquotes[i] = (data[i][2] + data[i][4]) / 2 

    return np.mean(midquotes)

# compute terminal price - average of last 5 mid-quote prices
def getTerminalPrice(data, n):
    midquotes = [None] * n
    
    for i in range(n):
        midquotes[i] = (data[-(i+1)][2] + data[-(i+1)][4]) / 2

    return np.mean(midquotes)

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

# compute imbalance using the modified TickTest from impactModel
def getImbalance(data):
    tickTest = TickTest()
    classifications = tickTest.classifyAll( data, times['9:30'], times['15:30'] )
    
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
            dw[k]['ticker'] = k;
            w.writerow({field: dw[k].get(field) or '' for field in fields})

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

""" TO SPECIFY """
output = '/media/louis/DATA/documents/cours/NYU/SPRING_18/ATQS/HK1/stats'

""" TO SPECIFY """
list_tickers_xls = pd.read_excel(open(tickers_todo,'rb'), sheet_name='Michael')
list_tickers = np.unique((np.array(list_tickers_xls['Ticker Symbol'])).astype(str))
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
dates.sort()

stats = {}
for key in keys:
    stats[key] = {} 
    for ticker in list_tickers:
        stats[key][ticker] = {}
        for i in range(D - 1):
            stats[key][ticker][dates[i]] = None
        
for i in range(D - 1):
    startDate = dates[i]
    endDate = dates[i+1]
    j = 0
    
    print(startDate)
    startTime = time.time()
     
    for ticker in list_tickers:
        try:
            j += 1
            if not os.path.exists(os.path.join(filepathcln, 'quotes', startDate, ticker + "_quotes.binRQ")):
                continue
            stack = StackData(filepathcln, startDate, endDate, ticker)
            stack.addQuotes()
            stack.addTrades()
             
            quotes = stack.getStackedQuotes()
            trades = stack.getStackedTrades() 
             
            stats['arrival_price'][ticker][startDate] = getArrivalPrice(quotes, 5)
            stats['imbalance'][ticker][startDate] = getImbalance(trades)      
            stats['terminal_price'][ticker][startDate] = getTerminalPrice(quotes, 5) 
            stats['VWAPuntil330'][ticker][startDate] = getVWAP(trades, times['9:30'], times['15:30'])
            stats['VWAPuntil400'][ticker][startDate] = getVWAP(trades, times['9:30'], times['16:00'])     
            stats['vol'][ticker][startDate] = getTotalDailyVol(trades)
            stats['imbalance_value'][ticker][startDate] = stats['imbalance'][ticker][startDate] * stats['VWAPuntil400'][ticker][startDate]
            
            quoteReturns = getXMinMidQuoteRet(quotes, times['2min'])
            stats['2_minute_returns'][ticker][startDate] = quoteReturns
            stats['std_2_min_returns'][ticker][startDate] = getSTDXMinMidQuoteRet(quoteReturns)
            
        except Exception as e:
            print("!!!! Failed processing ticker: {:s} : {:s}".format(ticker, str(e)))
    
    endTime = time.time()
    print('Completed in {:.1f}s'.format((endTime - startTime)))

# print(json.dumps(stats, indent=2, sort_keys=True))
 
# Export to Excel
print('Exporting...')
writer = pd.ExcelWriter(output + '/stats.xlsx')
for key in keys: 
    exportToCSV(stats, key)
    df = pd.read_csv(output + '/' + key + '.csv', index_col=0)
    df.to_excel(writer, sheet_name=key)
writer.save()    
print('Done...')
#     
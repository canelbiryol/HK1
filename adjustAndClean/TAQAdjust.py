import pandas as pd
import numpy as np
import struct
import gzip
import os.path
from os import access, R_OK

class TAQAdjust(object):
    '''
    Adjust prices, quotes and number of shares for corporate actions such as 
    stock splits/etc. by using the “Cumulative Factor to Adjust Prices” and 
    “Cumulative Factor to Adjust Shares/Vol” (see, “sp500.xlsx”). Note that
    if these factors did not change for a particular stock during the period,
    then no adjustment is necessary.
    '''

    def __init__(self, stackedQuotes, stackedTrades, s_p500):
        '''
        stackedQuotes: Array containing quotes (from StackData)
        stackedTrades: Array containing trades (from StackData)
        s_p500: String path to the s_p500.xlsx file
        '''
        # Instantiate attributes
        self._s_p500xls = pd.read_excel(open(s_p500,'rb'), sheet_name='WRDS')
        self._quotes = stackedQuotes
        self._trades = stackedTrades
        self._ticker = self._trades[0,1]
        
        # Retrieve quote multipliers from the excel file, and map them to each date
        allDates = []
        allDates = np.append(allDates, self._quotes[:,0], axis=0)
        allDates = np.append(allDates, self._trades[:,0], axis=0)
        allDates = np.unique(allDates)
        length = len(allDates)
        self._Mult = pd.DataFrame(np.zeros((length,2)))
        self._Mult.index = np.unique(self._quotes[:,0])
        for date in self._Mult.index:
            datePriceMult = float(self._s_p500xls[(self._s_p500xls['Names Date'] == float(date)) & (self._s_p500xls['Ticker Symbol'] == self._ticker)]['Cumulative Factor to Adjust Prices'])
            dateVolMult = float(self._s_p500xls[(self._s_p500xls['Names Date'] == float(date)) & (self._s_p500xls['Ticker Symbol'] == self._ticker)]['Cumulative Factor to Adjust Shares/Vol'])
            self._Mult.loc[date] = [ datePriceMult, dateVolMult ]

    # Apply price and volume multipliers to quotes data
    def adjustQuote(self):
        length = self._quotes.shape[0]
        
        for i in range(0, length):
            quote = self._quotes[i,:]
            date = quote[0]
            pMult = self._Mult.loc[date,0]
            vMult = self._Mult.loc[date,1]
            
            self._quotes[i, -1] = vMult * float(quote[-1])
            self._quotes[i, -2] = pMult * float(quote[-2])
            self._quotes[i, -3] = vMult * float(quote[-3])
            self._quotes[i, -4] = pMult * float(quote[-4])

    # Apply price and volume multipliers to trades data
    def adjustTrade(self):
        length = self._trades.shape[0]
        
        for i in range(0, length):
            trade = self._trades[i,:]
            date = trade[0]
            pMult = self._Mult.loc[date,0]
            vMult = self._Mult.loc[date,1]
            
            self._trades[i,-1] = vMult * float(trade[-1])
            self._trades[i, -2] = pMult * float(trade[-2])


    def getStackedQuotes(self):
        return(self._quotes)

    def getStackedTrades(self):
        return(self._trades)
        
    def getVolMult(self, date):
        return(self._Mult.loc[date, 1])
    
    def getPriceMult(self, date):
        return(self._Mult.loc[date, 0])
    
    # For the purpose of unit testing
    def setPriceMult(self, date, val):
        self._Mult.loc[date, 0] = val
        
    # For the purpose of unit testing
    def setVolMult(self, date, val):
        self._Mult.loc[date, 1] = val
        
    def storeAdjustedTrades(self, filepath):
        
        if not filepath.endswith('/'):
            filepath = filepath + "/"
        if not os.path.exists( filepath ):
            raise Exception( "%s does not exist" % filepath )
        if( not access( filepath, R_OK ) ):
            raise Exception( "You don't have access to directory %s" % filepath )
        
        filepath = filepath + "trades/"
        
        if not os.path.exists(filepath):
            os.makedirs(filepath)
        
        filepath = filepath + self._ticker + "_trades.binRT"
        
        with gzip.open( filepath, 'wb+') as f:
            # We didn't keep the SecsFromEpocToMidn so we set it to 0 (to be able to read with the TAQReaders provided
            f.write(struct.pack(">i", 0))
            # Updated N (number of entries)
            N = self._trades.shape[0]
            f.write(struct.pack(">i", N))
            # Write timestamps
            for i in range(N):
                f.write(struct.pack(">i", int(self._trades[i,2])))
            # Write sizes (int... but could be float with multipliers)
            for i in range(N):
                f.write(struct.pack(">i", int(float(self._trades[i,4]))))
            # Write prices (floats)
            for i in range(N):
                f.write(struct.pack(">f", float(self._trades[i,3])))
        
    def storeAdjustedQuotes(self, filepath):

        if not filepath.endswith('/'):
            filepath = filepath + "/"
        if not os.path.exists( filepath ):
            raise Exception( "%s does not exist" % filepath )
        if( not access( filepath, R_OK ) ):
            raise Exception( "You don't have access to directory %s" % filepath )

        filepath = filepath + "quotes/"
        
        if not os.path.exists(filepath):
            os.makedirs(filepath)

        filepath = filepath + self._ticker + "_quotes.binRQ"

        with gzip.open( filepath, 'wb+') as f:
            # We didn't keep the SecsFromEpocToMidn so we set it to 0 (to be able to read with the TAQReaders provided
            f.write(struct.pack(">i", 0))
            # Updated N (number of entries)
            N = self._quotes.shape[0]
            f.write(struct.pack(">i", N))
            # Write timestamps
            for i in range(N):
                f.write(struct.pack(">i", int(self._quotes[i,2])))
            # Write bid sizes (int... but could be float with multipliers)
            for i in range(N):
                f.write(struct.pack(">i", int(float(self._quotes[i,4]))))
            # Write bid prices (floats)
            for i in range(N):
                f.write(struct.pack(">f", float(self._quotes[i,3])))
            # Write ask sizes (int... but could be float with multipliers)
            for i in range(N):
                f.write(struct.pack(">i", int(float(self._quotes[i,6]))))
            # Write ask prices (floats)
            for i in range(N):
                f.write(struct.pack(">f", float(self._quotes[i,5])))

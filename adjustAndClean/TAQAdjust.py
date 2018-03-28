import pandas as pd
import numpy as np
import struct
import gzip
import os.path
from os import access, R_OK
from adjustAndClean.AdjustingHashmap import AdjustingHashmap

class TAQAdjust(object):
    '''
    Adjust prices, quotes and number of shares for corporate actions such as 
    stock splits/etc. by using the “Cumulative Factor to Adjust Prices” and 
    “Cumulative Factor to Adjust Shares/Vol” (see, “sp500.xlsx”). Note that
    if these factors did not change for a particular stock during the period,
    then no adjustment is necessary.
    '''

    def __init__(self, stackedQuotes, stackedTrades, ticker, multMap):
        '''
        stackedQuotes: Array containing quotes (from StackData)
        stackedTrades: Array containing trades (from StackData)
        s_p500: String path to the s_p500.xlsx file
        '''
        # Instantiate attributes
        self._quotes = stackedQuotes
        self._trades = stackedTrades
        self._ticker = ticker
        self._multMap = multMap

    # Apply price and volume multipliers to quotes data
    def adjustQuote(self):
        
        vol_mults = np.array([self._multMap.getVolMultiplier(self._ticker, date) for date in self._quotes[:,0]])
        price_mults = np.array([self._multMap.getPriceMultiplier(self._ticker, date) for date in self._quotes[:,0]])

        self._quotes[:,-1] =  (self._quotes[:,-1]).astype(float) * vol_mults
        self._quotes[:,-2] =  (self._quotes[:,-2]).astype(float) * price_mults
        self._quotes[:,-3] =  (self._quotes[:,-3]).astype(float) * vol_mults
        self._quotes[:,-4] =  (self._quotes[:,-4]).astype(float) * price_mults

    # Apply price and volume multipliers to trades data
    def adjustTrade(self):

        volt_mults = np.array([self._multMap.getVolMultiplier(self._ticker, date) for date in self._trades[:,0]])
        pricet_mults = np.array([self._multMap.getPriceMultiplier(self._ticker, date) for date in self._trades[:,0]])

        self._trades[:,-1] =  (self._trades[:,-1]).astype(float) * volt_mults
        self._trades[:,-2] =  (self._trades[:,-2]).astype(float) * pricet_mults

    def getStackedQuotes(self):
        return(self._quotes)

    def getStackedTrades(self):
        return(self._trades)
        
    def getVolMult(self, date):
        return(self._multMap.getVolMultiplier(self._ticker, date))
    
    def getPriceMult(self, date):
        return(self._multMap.getPriceMultiplier(self._ticker, date))
    
    # For the purpose of unit testing
    def setPriceMult(self, date, val):
        self._multMap.setPriceMultiplier(self._ticker, date, val)
        
    # For the purpose of unit testing
    def setVolMult(self, date, val):
        self._multMap.setVolMultiplier(self._ticker, date, val)
        
    def storeAdjustedTrades(self, filepath):
        
        if not filepath.endswith('/'):
            filepath = filepath + "/"
        if not os.path.exists( filepath ):
            raise Exception( "%s does not exist" % filepath )
        if( not access( filepath, R_OK ) ):
            raise Exception( "You don't have access to directory %s" % filepath )
        
        filepath = filepath  + "trades/" + self._trades[0,0] + "/"

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
                f.write(struct.pack(">i", int(self._trades[i,1])))
            # Write sizes (int... but could be float with multipliers)
            for i in range(N):
                f.write(struct.pack(">i", int(float(self._trades[i,3]))))
            # Write prices (floats)
            for i in range(N):
                f.write(struct.pack(">f", float(self._trades[i,2])))
        
    def storeAdjustedQuotes(self, filepath):

        if not filepath.endswith('/'):
            filepath = filepath + "/"
        if not os.path.exists( filepath ):
            raise Exception( "%s does not exist" % filepath )
        if( not access( filepath, R_OK ) ):
            raise Exception( "You don't have access to directory %s" % filepath )
        
        filepath = filepath  + "quotes/" + self._quotes[0,0] + "/"

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
                f.write(struct.pack(">i", int(self._quotes[i,1])))
            # Write bid sizes (int... but could be float with multipliers)
            for i in range(N):
                f.write(struct.pack(">i", int(float(self._quotes[i,3]))))
            # Write bid prices (floats)
            for i in range(N):
                f.write(struct.pack(">f", float(self._quotes[i,2])))
            # Write ask sizes (int... but could be float with multipliers)
            for i in range(N):
                f.write(struct.pack(">i", int(float(self._quotes[i,5]))))
            # Write ask prices (floats)
            for i in range(N):
                f.write(struct.pack(">f", float(self._quotes[i,4])))

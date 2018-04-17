import numpy as np
import struct
import gzip
import os.path
from os import access, R_OK

class TAQCleaner(object):
    '''
    Cleans an array of TAQ Data.
    The method gives the option to store the cleaned data to files.
    Default values for k and gamma were those given by the simulation (cf. CleanCalibration.py)
    '''

    def __init__(self, stackedQuotes, stackedTrades, ticker, kT=25, gammaT=0.0005, kQ=25, gammaQ=0.0005):
        '''
        Constructor: initialize attributes
        '''
        # Instantiate attributes
        self._quotes = stackedQuotes
        self._trades = stackedTrades
        self._ticker = ticker
        
        # Suggested initial parameters, to calibrate
        self._kT = kT
        self._gammaT = gammaT
        self._kQ = kQ
        self._gammaQ = gammaQ
        
    def rollingWindow(self, a, window):
        
        window = min(a.shape[-1], window)
        shape = a.shape[:-1] + (a.shape[-1] - window + 1, window)
        strides = a.strides + (a.strides[-1],)
        
        return np.lib.stride_tricks.as_strided(a, shape=shape, strides=strides)

    def cleanQuotesIndices(self):
        
        length = self._quotes.shape[0]
        
        midList = 0.5 * (np.array(self._quotes[0:length,-4].astype(np.float)) + np.array(self._quotes[0:length,-2].astype(np.float)))
        
        size = min(midList.shape[-1],self._kQ)
        roll = self.rollingWindow(midList,size)
        
        # BEFORE: roll = np.concatenate([np.tile(roll[0],(size - 1,1)), roll])
        # NOW: Center it (we want half of past and half of forward values)
        if ((size-1)%2 == 0):
            roll = np.concatenate([np.tile(roll[0],(int((size - 1)/2),1)), np.concatenate([roll, np.tile(roll[-1],(int((size - 1)/2),1))])])
        else:
            roll = np.concatenate([np.tile(roll[0],((int(size/2) - 1),1)), np.concatenate([roll, np.tile(roll[-1],((int(size/2)),1))])])
        
        rollMeanMidVector, rollStdMidVector = np.mean(roll, -1).flatten(), np.std(roll,-1).flatten()
        
        indices_kept = (abs(midList - rollMeanMidVector) <= 2 * rollStdMidVector + self._gammaQ * rollMeanMidVector)
        return(indices_kept)
        
                    
    def cleanTradesIndices(self):

        length = self._trades.shape[0]
        
        windowTrade = np.array(self._trades[0:length,-2].astype(np.float))
        
        size = min(windowTrade.shape[-1],self._kT)
        roll = self.rollingWindow(windowTrade,size)

        # BEFORE: roll = np.concatenate([np.tile(roll[0],(size - 1,1)), roll])
        # NOW: Center it (we want half of past and half of forward values)
        if ((size-1)%2 == 0):
            roll = np.concatenate([np.tile(roll[0],(int((size - 1)/2),1)), np.concatenate([roll, np.tile(roll[-1],(int((size - 1)/2),1))])])
        else:
            roll = np.concatenate([np.tile(roll[0],((int(size/2) - 1),1)), np.concatenate([roll, np.tile(roll[-1],((int(size/2)),1))])])
            
        rollMeanMidVector, rollStdMidVector = np.mean(roll, -1).flatten(), np.std(roll, -1).flatten()
        
        indices_kept = (abs(windowTrade - rollMeanMidVector) <= 2 * rollStdMidVector + self._gammaT * rollMeanMidVector)
        return(indices_kept)

        
    def storeCleanedTrades(self, filepath):
        
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

    def storeCleanedQuotes(self, filepath):

        if not filepath.endswith('/'):
            filepath = filepath + "/"
        if not os.path.exists( filepath ):
            raise Exception( "%s does not exist" % filepath )
        if( not access( filepath, R_OK ) ):
            raise Exception( "You don't have access to directory %s" % filepath )
        
        filepath = filepath + "quotes/" + self._quotes[0,0] + "/"

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
        
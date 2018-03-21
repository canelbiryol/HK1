import unittest
import gzip
import struct
import numpy as np

class Test_WriteBinaryFile(unittest.TestCase):
    '''
    This class tests the functionality of the methods addQuotes and addTrades of the class StackData.
    It works on the base directory provided by the user, and apply them to the IBM ticker.
    '''

    def test1(self):
        stackedTrades = np.array([['20070620', 34241000, 106.5, 85200.0], ['20070621', 57596000, 106.61000061035156, 500.0], ['20070621', 57596000, 106.61000061035156, 200.0], ['20070621', 57597000, 106.5999984741211, 200.0], ['20070621', 57597000, 106.5999984741211, 200.0], ['20070621', 57597000, 106.5999984741211, 200.0]])
        stackedQuotes = np.array([['20070620', 34241000, 106.5, 85200.0, 106.1, 8200.0], ['20070621', 57597000, 106.5, 85200.0, 106.1, 800.0], ['20070621', 57597000, 106.5, 85200.0, 106.1, 800.0], ['20070621', 57597000, 106.5, 85200.0, 106.1, 800.0], ['20070621', 57597000, 106.5, 85200.0, 106.1, 800.0]])
        
        filePathNameT = '/media/louis/DATA/documents/cours/NYU/SPRING_18/ATQS/HK1/test.binRT'
        filePathNameQ = '/media/louis/DATA/documents/cours/NYU/SPRING_18/ATQS/HK1/test.binRQ'
        
        # Trades
        with gzip.open( filePathNameT, 'wb+') as f:
            # We didn't keep the SecsFromEpocToMidn so we set it to 0 (to be able to read with the TAQReaders provided
            f.write(struct.pack(">i", 0))
            # Updated N (number of entries)
            N = stackedTrades.shape[0]
            f.write(struct.pack(">i", N))
            # Write timestamps
            for i in range(N):
                f.write(struct.pack(">i", int(stackedTrades[i,1])))
            # Write sizes (int... but could be float with multipliers)
            for i in range(N):
                f.write(struct.pack(">i", int(float(stackedTrades[i,3]))))
            # Write prices (floats)
            for i in range(N):
                f.write(struct.pack(">f", float(stackedTrades[i,2])))
        
        # Try reading trade file
        with gzip.open( filePathNameT, 'rb') as f:
            content = f.read()
            print(struct.unpack_from(( ">2i"  ), content[ 0:8 ]))
            print(struct.unpack_from(( ">%di" % N ), content[ 8: (8 + N*4) ]))
            print(struct.unpack_from(( ">%di" % N ), content[ (8 + 4*N) : (8 + 8*N)]))
            print(struct.unpack_from(( ">%df" % N ), content[ (8 + 8*N) : (8 + 12*N) ]))
            
        # Trades
        with gzip.open( filePathNameQ, 'wb+') as f:
            # We didn't keep the SecsFromEpocToMidn so we set it to 0 (to be able to read with the TAQReaders provided
            f.write(struct.pack(">i", 0))
            # Updated N (number of entries)
            N = stackedQuotes.shape[0]
            f.write(struct.pack(">i", N))
            # Write timestamps
            for i in range(N):
                f.write(struct.pack(">i", int(stackedQuotes[i,1])))
            # Write bid sizes (int... but could be float with multipliers)
            for i in range(N):
                f.write(struct.pack(">i", int(float(stackedQuotes[i,3]))))
            # Write bid prices (floats)
            for i in range(N):
                f.write(struct.pack(">f", float(stackedQuotes[i,2])))
            # Write ask sizes (int... but could be float with multipliers)
            for i in range(N):
                f.write(struct.pack(">i", int(float(stackedQuotes[i,5]))))
            # Write ask prices (floats)
            for i in range(N):
                f.write(struct.pack(">f", float(stackedQuotes[i,4])))
                
        # Try reading quote file
        with gzip.open( filePathNameQ, 'rb') as f:
            content = f.read()
            print(struct.unpack_from(( ">2i"  ), content[ 0:8 ]))
            print(struct.unpack_from(( ">%di" % N ), content[ 8: (8 + 4*N) ]))
            print(struct.unpack_from(( ">%di" % N ), content[ (8 + 4*N) : (8 + 8*N)]))
            print(struct.unpack_from(( ">%df" % N ), content[ (8 + 8*N) : (8 + 12*N) ]))
            print(struct.unpack_from(( ">%di" % N ), content[ (8 + 12*N) : (8 + 16*N)]))
            print(struct.unpack_from(( ">%df" % N ), content[ (8 + 16*N) : (8 + 20*N) ]))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test1']
    unittest.main()
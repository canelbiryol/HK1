class TickTest(object):
    '''
    This class implements the tick test for inferring the direction
    of trades.
    '''
    TOLERANCE = 0.00001

    def __init__(self):
        self.side = 0
        self.prevPrice = 0
        
    def classify(self, newPrice):
        if( self.prevPrice != 0 ):
            if( newPrice > ( self.prevPrice + type(self).TOLERANCE ) ):
                self.side = 1
            else:
                if( newPrice < ( self.prevPrice - type( self ).TOLERANCE ) ):
                    self.side = -1
        self.prevPrice = newPrice
        return( self.side )
    
    #cb
    #modified the method to return timestamp, trade size and classification
    def classifyAll(self, data, startTimestamp, endTimestamp ):
        classifications = [0]*len(data) # That's the most space we might need
        startI = 0
        for i in range( 0, len(data) ):
            if( data[i][1] < startTimestamp ):
                continue
            if( data[i][1] >= endTimestamp ):
                break
            classifications[ startI ] = ( data[i][1], data[i][3], self.classify( data[i][2] ) )
            startI = startI + 1
        return classifications[0:startI]
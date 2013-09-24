import cPickle

PATH_DATABASE = 'SAN_minutes.pkl'

class Stock:
    ''' handling of pkl files representing stocks '''
    def __init__(self, stockName, compresion = 'minutes'):
        # load stock from disk
        f = open(PATH_DATABASE + stockName + '_' + compresion + '.pkl','rb')
        s = cPickle.load(f)
        # info
        self.name   = s['name']
        self.compresion = compresion
        # data lists
        self.opens   = s['open']
        self.closes  = s['close']
        self.highs   = s['high']
        self.lows    = s['low']    
        self.volumes = s['volume']
        self.dates   = s['date']

    def show(self):
        import matplotlib.pyplot as plt
        d = self.dates[0]
        print 'Plotting minutes of ',d.date(), ' or day', d.day, 'hour', d.hour, 'minute', d.minute
        nMinutes = 1000
        plt.plot(self.closes[0:nMinutes])

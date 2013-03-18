import ystockquote
from pylab import *
import math

def average(x):
    assert len(x) > 0
    return float(sum(x)) / len(x)

def pearson_def(x, y):
    assert len(x) == len(y)
    n = len(x)
    assert n > 0
    avg_x = average(x)
    avg_y = average(y)
    diffprod = 0
    xdiff2 = 0
    ydiff2 = 0
    for idx in range(n):
        xdiff = x[idx] - avg_x
        ydiff = y[idx] - avg_y
        diffprod += xdiff * ydiff
        xdiff2 += xdiff * xdiff
        ydiff2 += ydiff * ydiff

    return diffprod / math.sqrt(xdiff2 * ydiff2)

#Correlation through time
def chunks(l, n):
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

# Get Quotes 01/01/2006 - 01/01/2009
GOOG = ystockquote.get_historical_prices('AAPL', '20060101', '20110101')

# Create empty lists, quick and dirty
GOOGOpen = [ ]
GOOGClose = [ ]
GOOGDate = [ ]
GOOGHigh = [ ]
GOOGLow = [ ]
GOOGAdj = [ ]
GOOGVolume = [ ]

# Populate lists from downloaded data
for i in range(1, 1255):
  GOOGDate.append(GOOG[i][0])
  GOOGOpen.append(GOOG[i][1])
  GOOGHigh.append(GOOG[i][2])
  GOOGLow.append(GOOG[i][3])
  GOOGClose.append(float(GOOG[i][4]))
  GOOGVolume.append(GOOG[i][5])
  GOOGAdj.append(float(GOOG[i][6]))

VIX = ystockquote.get_historical_prices('^VIX', '20060101', '20110101')

VIXClose = []
for i in range(1, 1255):
  VIXClose.append(float(VIX[i][4]))

normalizedscores = array([float(u)/max(VIXClose) for u in VIXClose])
VIXClose = normalizedscores
GOOGClose = array([float(u)/max(GOOGClose) for u in GOOGClose])
corr = pearson_def(GOOGClose, VIXClose)
VIXChunked = list(chunks(VIXClose, 160))
GOOGLEChunked = list(chunks(GOOGClose, 160))

correlations = []
i = 0
for item in VIXChunked:
  correlations.append(pearson_def(item, GOOGLEChunked[i]))
  i = i + 1

plot(correlations)
title("Google Adjusted Close")
ylabel(r"GOOG Closing Price ($USD)", fontsize = 12)
xlabel(r"Date", fontsize = 12)
grid(True)
show()
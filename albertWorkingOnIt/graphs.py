
import matplotlib.pyplot as plt
   
def showGraph(stock):
    price = [day['close'] for day in stock.prices]
    volume = [day['volume'] for day in stock.prices]
    fig = plt.figure()
    ax = fig.add_subplot(311)
    ax2 = fig.add_subplot(312, sharex=ax)
    ax.plot(price)
    ax2.plot(volume)
    plt.show()


from pylab import *
from matplotlib.dates import  DateFormatter, WeekdayLocator, HourLocator, \
     DayLocator, MONDAY
from matplotlib.finance import quotes_historical_yahoo, candlestick,\
     plot_day_summary, candlestick2
from matplotlib.dates import date2num

def showCandles(stock, days):
    quotes = []
    prices = stock.prices[len(stock.prices)-days:]
    for day in prices:
        date = map(int,tuple(day['date'].split('-')))
        date = date2num(datetime.date(*date))
        quotes.append((date, float(day['open']), float(day['close']),float(day['high']),float(day['low'])))

    mondays = WeekdayLocator(MONDAY)        # major ticks on the mondays
    alldays    = DayLocator()              # minor ticks on the days
    weekFormatter = DateFormatter('%b %d')  # Eg, Jan 12
    dayFormatter = DateFormatter('%d')      # Eg, 12
    
    fig = figure()
    fig.subplots_adjust(bottom=0.2)
    ax = fig.add_subplot(111)
    ax.xaxis.set_major_locator(mondays)
    ax.xaxis.set_minor_locator(alldays)
    ax.xaxis.set_major_formatter(weekFormatter)
    #ax.xaxis.set_minor_formatter(dayFormatter)
    
    candlestick(ax, quotes, width=0.6)

    ax.xaxis_date()
    ax.autoscale_view()
    setp( gca().get_xticklabels(), rotation=45, horizontalalignment='right')

    show()
    
    
def candlestick(ax, quotes, width=0.2, colorup='w', colordown='k',
                alpha=1.0, usePrevious = False):

    """
Red/Black:
Red - Close is below close 1 day ago 


Black - Close is above close 1 day ago



Filled/Unfilled:
Filled - Close is below open


Unfilled - Close is above open

    quotes is a list of (time, open, close, high, low, ...)  tuples.
    As long as the first 5 elements of the tuples are these values,
    the tuple can be as long as you want (eg it may store volume).

    time must be in float days format - see date2num

    Plot the time, open, close, high, low as a vertical line ranging
    from low to high.  Use a rectangular bar to represent the
    open-close span.  If close >= open, use colorup to color the bar,
    otherwise use colordown

    ax          : an Axes instance to plot to
    width       : fraction of a day for the rectangle width
    colorup     : the color of the rectangle where close >= open
    colordown   : the color of the rectangle where close <  open
    alpha       : the rectangle alpha level

    return value is lines, patches where lines is a list of lines
    added and patches is a list of the rectangle patches added
    """


    OFFSET = width/2.0


    lines = []
    patches = []
    prev_close = None 
    for q in quotes:
        t, open, close, high, low = q[:5]
        
        if usePrevious:
            if not prev_close or close >= prev_close: 
                color_edge = colorup
            else:
                color_edge = colordown
        else:    
            color_edge = 'k'
            
        prev_close = close

        if close >= open :
            if usePrevious:
                color_body = 'w'
            else:
                color_body = colorup
            lower = open
            height = close-open
            vline1 = Line2D(
                xdata=(t, t), ydata=(close, high),
                color=color_edge,
                linewidth=0.5,
                antialiased=True,
                )
            vline2 = Line2D(
                xdata=(t, t), ydata=(open, low),
                color=color_edge,
                linewidth=0.5,
                antialiased=True,
                )
            
        else:
            if usePrevious:
                color_body = color_edge
            else:
                color_body = colordown
            lower = close
            height = open-close
            vline1 = Line2D(
                xdata=(t, t), ydata=(close, low),
                color=color_edge,
                linewidth=0.5,
                antialiased=True,
                )
            vline2 = Line2D(
                xdata=(t, t), ydata=(open, high),
                color=color_edge,
                linewidth=0.5,
                antialiased=True,
                )


        rect = Rectangle(
            xy    = (t-OFFSET, lower),
            width = width,
            height = height,
            facecolor = color_body,
            edgecolor = color_edge,
            )
        rect.set_alpha(alpha)


        lines.append(vline1)
        lines.append(vline2)
        patches.append(rect)
        ax.add_line(vline1)
        ax.add_line(vline2)
        ax.add_patch(rect)
    ax.autoscale_view()

    return lines, patches
    
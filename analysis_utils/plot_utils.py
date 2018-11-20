"""

Some utilities for plotting
"""

import datetime

import numpy as np
import pandas as pd

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.dates import num2date
from matplotlib.dates import date2num

from mpl_finance import candlestick_ochl as candlestick


# Credit to: ljk07 on Stack Overflow
def plot_candlestick_and_volume(data_df: pd.DataFrame):
    """ Plot a candlestick chart of open/high/low/close with the
        volume overlayed at the bottom

    :param data_df: pandas.DataFrame that requires columns: date, open, close,
        max, min, volume
    """

    candlesticks = zip(
        date2num(data_df['date']),
        data_df['open'], data_df['close'],
        data_df['max'], data_df['min'],
        data_df['volume'])

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    ax.set_ylabel('Quote ($)', size=20)
    candlestick(ax, candlesticks, width=1, colorup='g', colordown='r')

    # shift y-limits of the candlestick plot so that there is space at the bottom for the volume bar chart
    pad = 0.25
    yl = ax.get_ylim()
    ax.set_ylim(yl[0]-(yl[1]-yl[0])*pad, yl[1])

    # create the second axis for the volume bar-plot
    ax2 = ax.twinx()

    # set the position of ax2 so that it is short (y2=0.32)
    # but otherwise the same size as ax
    ax2.set_position(
        matplotlib.transforms.Bbox([[0.125, 0.1], [0.9, 0.32]]))

    # get data from candlesticks for a bar plot
    dates = [x[0] for x in candlesticks]
    dates = np.asarray(dates)
    volume = [x[5] for x in candlesticks]
    volume = np.asarray(volume)

    # make bar plots and color differently depending on up/down for the day
    pos = (data_df['open'] - data_df['close']) < 0
    neg = (data_df['open'] - data_df['close']) > 0
    ax2.bar(dates[pos], volume[pos], color='green', width=1, align='center')
    ax2.bar(dates[neg], volume[neg], color='red', width=1, align='center')

    # scale the x-axis tight
    ax2.set_xlim(min(dates), max(dates))
    # the y-ticks for the bar were too dense, keep only every third one
    yticks = ax2.get_yticks()
    ax2.set_yticks(yticks[::3])

    ax2.yaxis.set_label_position("right")
    ax2.set_ylabel('Volume', size=20)

    # format the x-ticks with a human-readable date.
    xt = ax.get_xticks()
    new_xticks = [datetime.date.isoformat(num2date(d)) for d in xt]
    ax.set_xticklabels(new_xticks, rotation=45, horizontalalignment='right')

    # plt.ion()
    # plt.show()
    return fig, ax

import talib

from yahooquery import Ticker


aapl= Ticker ("AAPL")
price= aapl.history()

aapl_adosc= talib.ADOSC (price["high"], price ["low"], price["close"], price["volume"], fastperiod=3, slowperiod=10)

from matplotlib import pyplot as plt
plt.plot(aapl_adosc)


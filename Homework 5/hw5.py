import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np





yahoodatabase=da.DataAccess('Yahoo')
syms=['AAPL','GOOG','IBM','MSFT']
keys=['actual_close','close']
start_date=dt.datetime(2010,01,01)
end_date=dt.datetime(2010,12,31)
delta_time=dt.timedelta(hours=16)
opentimes=du.getNYSEdays(start_date,end_date,delta_time)
prices=yahoodatabase.get_data(opentimes,syms,keys)
prices_dic=dict(zip(keys,prices))

for key in keys:
	prices_dic[key]=prices_dic[key].fillna(method='ffill')
	prices_dic[key]=prices_dic[key].fillna(method='bfill')
	prices_dic[key]=prices_dic[key].fillna(1.0)
	

prices_close=prices_dic['close']

roll_mean=pd.rolling_mean(prices_close,20)
roll_std=pd.rolling_std(prices_close,20)
Bol=(prices_close-roll_mean)/roll_std

Bol.to_csv('Bol.csv')

print 'The bollinger values have been saved to a csv file into your working directory.\n'

print'From the list of equities below, which one would you like to plot a graph for?\n'
print syms, '\n'
prompt=raw_input()

prices_close_input=prices_close.copy()
prices_close_input['Lower']=pd.rolling_mean(prices_close_input[prompt],20)-pd.rolling_std(prices_close_input[prompt],20)
prices_close_input['Upper']=pd.rolling_mean(prices_close_input[prompt],20)+pd.rolling_std(prices_close_input[prompt],20)
plt.clf()
fig, axes=plt.subplots(nrows=2)
prices_close_input[prompt].plot(ax=axes[0])
prices_close_input['Lower'].plot(ax=axes[0])
prices_close_input['Upper'].plot(ax=axes[0])
axes[0].fill_between(x=prices_close_input.index,y1=prices_close_input['Lower'],y2=prices_close_input['Upper'],facecolor='gray')
axes[0].legend([prompt,'LOWER','UPPER'],loc='best')
axes[0].autoscale()

Bol[prompt].plot(ax=axes[1])
axes[1].legend(['B.Vals of '+prompt],loc='best')
axes[1].axhline(y=-1,color='orange')
axes[1].axhline(y=1,color='orange')
axes[1].autoscale()
axes[1].fill_between(x=Bol.index,y1=-1,y2=1,facecolor='gray')
fig.subplots_adjust(hspace=0.5)
plt.savefig('hw5.pdf',format='pdf')
		

	
	
	

		



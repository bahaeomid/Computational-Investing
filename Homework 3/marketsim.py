import numpy as np
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import csv
import copy


orders_csv_pd=pd.read_csv('orders.csv',parse_dates={'Date':[0,1,2]},header=None)
orders_csv_np=orders_csv_pd.values[:,:-1]
syms=set(orders_csv_np[:,1])

for row in range(len(orders_csv_pd)):
	orders_csv_pd['Date'][row] += dt.timedelta(hours=16)

start_date=orders_csv_pd['Date'].min()
end_date=orders_csv_pd['Date'].max()
keys=['actual_close','close']
database=da.DataAccess('Yahoo')
closetime=dt.timedelta(hours=16)
opentimes=du.getNYSEdays(start_date,end_date,closetime)
prices=database.get_data(opentimes,syms,keys)
prices=dict(zip(keys,prices))
prices_close=prices['close']
prices_close=prices_close.fillna(method='ffill')
prices_close=prices_close.fillna(method='bfill')


cash=1000000
casharray=copy.deepcopy(prices_close)*0
casharray=casharray['GOOG']
own=copy.deepcopy(prices_close)*0
valuearray=casharray.copy()



for row in range(len(orders_csv_pd)):
        if orders_csv_pd.ix[row][4]=='Buy':
                own[orders_csv_pd.ix[row][3]][orders_csv_pd['Date'][row]:] += orders_csv_pd.ix[row][5]
                cash -= prices_close[orders_csv_pd.ix[row][3]][orders_csv_pd['Date'][row]]*orders_csv_pd.ix[row][5]
                casharray[orders_csv_pd['Date'][row]:] = cash
		
		        	
        if orders_csv_pd.ix[row][4]=='Sell':
                own[orders_csv_pd.ix[row][3]][orders_csv_pd['Date'][row]:] -= orders_csv_pd.ix[row][5]
                cash += prices_close[orders_csv_pd.ix[row][3]][orders_csv_pd['Date'][row]]*orders_csv_pd.ix[row][5]
                casharray[orders_csv_pd['Date'][row]:] = cash
		
		
		
		
value=np.sum(own.values*prices_close.values,axis=1)	
for i in range(len(valuearray)):
		valuearray[i]=value[i]

total=valuearray+casharray		
total.to_csv('total.csv')
		
print 'The final value of the portfolio using the sample file is as follows:\n',orders_csv_pd['Date'][len(orders_csv_pd['Date'])-1] ,'  ', cash,'\n'
print 'The file containing your daily portfolio value has been saved to your working direcotry.\n'

user_input=raw_input('Enter the date to get the total value of the portfolio for that day: (YYYY-MM-DD)\n')
print '\n',total[user_input]

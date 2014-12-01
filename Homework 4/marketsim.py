import numpy as np
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import csv
import copy
from dateutil import parser


orders_csv_pd=pd.read_csv('orders.csv')
orders_csv_pd=orders_csv_pd.sort(['Date'])
orders_csv_pd=orders_csv_pd.reset_index(drop=True)
orders_csv_np=orders_csv_pd.values[:,1:]
syms=set(orders_csv_np[:,1])

for i in range(len(orders_csv_pd['Date'])):
        orders_csv_pd['Date'][i]=parser.parse(orders_csv_pd['Date'][i])
        
orders_csv_pd['Date']=pd.DatetimeIndex(orders_csv_pd['Date'])

start_date=orders_csv_pd['Date'].min()-dt.timedelta(hours=16)
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


cash=50000
casharray=copy.deepcopy(prices_close)*0
casharray=casharray[list(syms)[0]]
own=copy.deepcopy(prices_close)*0
valuearray=casharray.copy()



for row in range(len(orders_csv_pd)):
        if orders_csv_pd.ix[row]['Order']=='Buy':
                own[orders_csv_pd.ix[row]['Sym']][orders_csv_pd['Date'][row]:] += orders_csv_pd.ix[row]['Qty']
                cash -= prices_close[orders_csv_pd.ix[row]['Sym']][orders_csv_pd['Date'][row]]*orders_csv_pd.ix[row]['Qty']
                casharray[orders_csv_pd['Date'][row]:] = cash
                
		
		        	
        if orders_csv_pd.ix[row]['Order']=='Sell':
                own[orders_csv_pd.ix[row]['Sym']][orders_csv_pd['Date'][row]:] -= orders_csv_pd.ix[row]['Qty']
                cash += prices_close[orders_csv_pd.ix[row]['Sym']][orders_csv_pd['Date'][row]]*orders_csv_pd.ix[row]['Qty']
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

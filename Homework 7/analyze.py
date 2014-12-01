import pandas as pd
import matplotlib.pyplot as plt
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da
import datetime as dt
from dateutil import parser
import numpy as np


values=pd.read_csv('total.csv',names=['Date','Value'])
values=values.sort(['Date'])
values=values.reset_index(drop=True)
start_date=values['Date'].min()
start_date=parser.parse(start_date)
end_date=values['Date'].max()
end_date=parser.parse(end_date)
closetime=dt.timedelta(hours=16)
opentimes=du.getNYSEdays(start_date,end_date,closetime)
yahoodatabase=da.DataAccess('Yahoo')
syms=['$SPX']
keys=['close','actual_close']
spx=yahoodatabase.get_data(opentimes,syms,keys)
spx=dict(zip(keys,spx))
spx=spx['close']

	


spx_norm=spx/spx.ix[0]
values_norm=values['Value']/values['Value'][0]

plt.clf()
fig=plt.figure()
fig.add_subplot(111)
plt.plot(pd.DatetimeIndex(values['Date']),values_norm)
plt.plot(pd.DatetimeIndex(values['Date']),spx_norm)
plt.ylabel('Price')
plt.xlabel('Date')
plt.legend(['Portfolio','SPX'],loc='upper left')
fig.autofmt_xdate(rotation=45)
plt.savefig('graph.pdf',format='pdf')
print '\nThe figure comparing the value of your portfolio against SPX has been saved and located in your working directory.'

ret_port=values_norm.copy()
ret_port=tsu.returnize0(ret_port)
std_port=np.std(ret_port)
ret_port_mean=np.mean(ret_port)
ret_spx=spx_norm.copy()
ret_spx=tsu.returnize0(ret_spx)
std_spx=np.std(ret_spx,axis=0)
ret_spx_mean=np.mean(ret_spx,axis=0)
risk_free=0
sharpe_port=np.sqrt(252)*((ret_port_mean-risk_free)/std_port)
sharpe_spx=np.sqrt(252)*((ret_spx_mean-risk_free)/std_spx)
cumret_port=np.cumprod(ret_port + 1,axis=0)
cumret_spx=np.cumprod(ret_spx.values + 1,axis=0)

print '\nDetails of the Performance of the portfolio :\n\n','Sharpe Ratio of Fund:\t',float(sharpe_port),'\nSharpe Ratio of $SPX:\t',float(sharpe_spx),'\n\nTotal Return of Fund:\t',float(cumret_port[-1]),'\nTotal Return of $SPX:\t',float(cumret_spx[-1]),'\n\nStandard Deviation of Fund:\t',float(std_port),'\nStandard Deviation of $SPX:\t',float(std_spx),'\n\nAverage Daily Return of Fund:\t',float(ret_port_mean),'\nAverage Daily Return of $SPX:\t',float(ret_spx_mean)




import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import QSTK.qstkstudy.EventProfiler as ep
import copy



yahoodatabase=da.DataAccess('Yahoo')
syms=yahoodatabase.get_symbols_from_list('sp5002012')
syms.append('SPY')
keys=['actual_close','close']
start_date=dt.datetime(2008,01,01)
end_date=dt.datetime(2009,12,31)
delta_time=dt.timedelta(hours=16)
opentimes=du.getNYSEdays(start_date,end_date,delta_time)
prices=yahoodatabase.get_data(opentimes,syms,keys)
prices_dic=dict(zip(keys,prices))

for key in keys:
	prices_dic[key]=prices_dic[key].fillna(method='ffill')
	prices_dic[key]=prices_dic[key].fillna(method='bfill')
	prices_dic[key]=prices_dic[key].fillna(1.0)
	

prices_close_all=prices_dic['close']

roll_mean=pd.rolling_mean(prices_close_all,20)
roll_std=pd.rolling_std(prices_close_all,20)
Bol=(prices_close_all-roll_mean)/roll_std


events=copy.deepcopy(Bol)
events=events*np.NAN

for sym in syms:
	for i in range(1,len(opentimes)):
		Bol_today=Bol[sym][i]
		Bol_yes=Bol[sym][i-1]
		Bol_SPY_today=Bol['SPY'][i]
				
		if Bol_today<-2.0 and Bol_yes>=-2.0 and Bol_SPY_today>=1.3:
			events[sym][i]=1
			
ep.eventprofiler(events, prices_dic, i_lookback=20, i_lookforward=20,
                s_filename='MyEventStudy.pdf', b_market_neutral=True, b_errorbars=True,
                s_market_sym='SPY')
		



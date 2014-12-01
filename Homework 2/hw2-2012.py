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
	

prices_actclose_all=prices_dic['actual_close']
prices_actclose_SPY=prices_actclose_all['SPY']

events=copy.deepcopy(prices_actclose_all)
events=events*np.NAN

for sym in syms:
	for i in range(1,len(opentimes)):
		price_sym_today=prices_actclose_all[sym][i]
		price_sym_yes=prices_actclose_all[sym][i-1]
		
		if price_sym_today<5.0 and price_sym_yes>=5.0:
			events[sym][i]=1
			
ep.eventprofiler(events, prices_dic, i_lookback=20, i_lookforward=20,
                s_filename='MyEventStudy.pdf', b_market_neutral=True, b_errorbars=True,
                s_market_sym='SPY')
		



import numpy as np
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd


class portHW1:
	def __init__(self,start_date,end_date,syms,weights):
		self.syms=syms
		self.weights=np.array(weights)
		if len(syms)!=len(self.weights):
			print 'ERROR!!!!\n\n',syms, 'and', weights, 'are not of the same length\n'
		if sum(weights) != 1 :
			print 'ERROR!!!!\n\n','Weights must add up to 1.\n'
		self.start_date=dt.datetime.strptime(start_date,'%Y-%m-%d')
		self.end_date=dt.datetime.strptime(end_date,'%Y-%m-%d')		
	def ReadPrices(self):
		yahoodatabase=da.DataAccess('Yahoo')
		closetime=du.timedelta(hours=16)
		opentimes=du.getNYSEdays(self.start_date,self.end_date,closetime)
		keys=['close','actual_close']
		readprices=yahoodatabase.get_data(opentimes,self.syms,keys)
		self.readprices=dict(zip(keys,readprices))
		return self.readprices
	def PortStats(self,risk_free=0):
		rets=self.readprices['close'].copy()
		rets=tsu.returnize0(rets)
		w=self.weights.copy()
		port_ret_daily=np.sum(w*rets,axis=1)
		port_ret_daily_mean=np.mean(port_ret_daily)
		port_ret_daily_std=np.std(port_ret_daily)
		port_cumret=np.cumprod(port_ret_daily + 1, axis=0)
		port_sharpe=np.sqrt(252)*((port_ret_daily_mean-risk_free)/port_ret_daily_std)
		print 'Start Date:\t',self.start_date,'\nEnd Date:\t', self.end_date,'\nSymbols:\t',self.syms,'\nOptimal Allocations:\t', self.weights,'\nSharpe Ratio:\t',port_sharpe,'\nVolatility:\t', port_ret_daily_std,'\nAverage Daily Return:\t',port_ret_daily_mean,'\nCumulative Return:\t', port_cumret[-1]
	
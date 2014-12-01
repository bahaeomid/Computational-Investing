import numpy as np
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd

'''This program reads the prices from QSTK database for an equity and calculates portfolio statistics'''

start_date=raw_input('What is the start date of your investment horizon? (YYYY-MM-DD)\n')
end_date=raw_input('What is the end date of your investment horizon? (YYYY-MM-DD)\n')
syms=input('What are the symbols of equities? (as a list of strings)\n')
weights=input('What are the initial allocations of your target portfolio? (as a list of weights)\n')

class portHW1:
	''' Creates a portfolio as per Homework 1, based on buy-and-hold assumption. The inputs are start and end dates, equity symbols and allocations/weights.'''
	def __init__(self,start_date,end_date,syms,weights):
		'''Initializes the class by defining the start and end dates, equity symbols and allocations/weights.'''
		self.syms=syms
		self.weights=np.array(weights)
		if len(syms)!=len(self.weights):
			print '\nERROR!!!!\nsymbols and weights are not of the same length\n'
			raise SystemExit
		if sum(weights) != 1 :
			print '\nERROR!!!!\nWeights must add up to 1.\n'
			raise SystemExit
		self.start_date=dt.datetime.strptime(start_date,'%Y-%m-%d')
		self.end_date=dt.datetime.strptime(end_date,'%Y-%m-%d')		
	def ReadPrices(self):
		'''Reads the actual and adjusted close prices from QSTK local yahoo database.'''
		yahoodatabase=da.DataAccess('Yahoo')
		closetime=du.timedelta(hours=16)
		self.opentimes=du.getNYSEdays(self.start_date,self.end_date,closetime)
		keys=['close','actual_close']
		readprices=yahoodatabase.get_data(self.opentimes,self.syms,keys)
		self.readprices=dict(zip(keys,readprices))
		return self.readprices
	def PortStats(self,risk_free=0):
		'''Calculates portfolio statistics namely average daily return, standard deviation, cumulative daily return and the porfolio sharpe ratio.'''
		prices=np.array(self.readprices['close'].copy())
		norm_prices=prices/prices[0,:]
		w=self.weights.copy()
		daily=np.sum(w*prices,axis=1)
		self.dailyp=daily/daily[0]
		port_price_daily=np.sum(w*norm_prices,axis=1)
		port_ret_daily=tsu.returnize0(port_price_daily)
		port_ret_daily_mean=np.mean(port_ret_daily)
		port_ret_daily_std=np.std(port_ret_daily)
		port_cumret=np.cumprod(port_ret_daily + 1, axis=0)
		port_sharpe=np.sqrt(252)*((port_ret_daily_mean-risk_free)/port_ret_daily_std)
		print '\nHere is the summary of the portfolio statistics:\n\nStart Date:\t',self.start_date,'\nEnd Date:\t', self.end_date,'\nSymbols:\t',self.syms,'\nOptimal Allocations:\t', self.weights,'\nSharpe Ratio:\t',port_sharpe,'\nVolatility:\t', port_ret_daily_std,'\nAverage Daily Return:\t',port_ret_daily_mean,'\nCumulative Return:\t', float(port_cumret[-1])
	def compare(self):
		'''compares the value of the portfolio against the market.'''
		spy_price=portHW1(self.start_date.strftime('%Y-%m-%d'),self.end_date.strftime('%Y-%m-%d'),['SPY'],[1]).ReadPrices()['close']
		spy_price_norm=np.array(spy_price)
		spy_price_norm=spy_price_norm/spy_price_norm[0]
		plt.clf()
		fig=plt.figure()
		fig.add_subplot(111)
		plt.plot(self.opentimes, spy_price_norm)
		plt.plot(self.opentimes,self.dailyp)
		plt.ylabel('Normalized Price')
		plt.xlabel('Date')
		plt.legend(['SPY','Portfolio'],loc='upper left')
		fig.autofmt_xdate(rotation=45)
		plt.savefig('graph.pdf',format='pdf')
		
myport=portHW1(start_date,end_date,syms,weights)
prices=myport.ReadPrices()
stats=myport.PortStats()
myport.compare()
print '\nThe figure comparing the value of your portfolio against SPY has been saved and located in your working directory.'
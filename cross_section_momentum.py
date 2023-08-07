# cross section momentum strategy
import yfinance as yf 
import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt

import requests
from bs4 import BeautifulSoup
import random
import numpy as np

from Para import Para 

para = Para()

num_day = para.mom_day 
num_high = para.num_high 
num_low = para.num_low 

mom_day = 36
num_high = 30
num_low = 30

data = pd.read_csv('randomstock150.csv')

#Calculate the return
returns_data = data.copy()
returns_data = returns_data.apply(func = lambda x: x.shift(-1)/x - 1, 
                                  axis = 0)

end_date = '2022-12-31'
date_range = pd.date_range(end = end_date, periods=len(data))

#Calculate Momentum Signal
mom_sig = data.copy()
mom_sig = mom_sig.apply(func = lambda x : x / x.shift(mom_day) -1 , 
                        axis = 0 )
mom_sig = mom_sig.rank(axis = 1)

#for col in mom_sig:
for col in mom_sig.columns:
    mom_sig[col] = np.where(mom_sig[col] >= num_high, 1, 
                            np.where(mom_sig[col] <= num_low, -1, 0))

return_sig = returns_data * mom_sig
portf_returns = pd.DataFrame(index = mom_sig.index, columns = ['ls'])
portf_returns = return_sig.sum(axis = 1) / (num_high + num_low)
portf_cum_returns = np.exp(np.log1p(portf_returns).cumsum())

pltdf = pd.DataFrame({'Date':date_range, 'portf_cum_returns':portf_cum_returns})

pltdf['Date'] = pd.to_datetime(pltdf['Date'])
pltdf.set_index('Date', inplace=True)
pltdf.plot(kind='line',figsize=(10, 5))


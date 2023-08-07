import yfinance as yf 
import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt

import requests
from bs4 import BeautifulSoup
import random
import numpy as np

response = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
soup = BeautifulSoup(response.text, 'html.parser')

# Extract the ticker symbols
ticker_symbols = []
for row in soup.find('table').find_all('tr')[1:]:
    ticker = row.find_all('td')[0].text.strip()
    ticker_symbols.append(ticker)

random_tickers = random.sample(ticker_symbols, 100)

begin_date = '2010-01-01'
end_date = '2022-12-31'


data = pd.DataFrame()

for ticker in random_tickers:
    df = yf.download(ticker, start=begin_date, end=end_date)
    data[ticker] = df['Close']

data.to_csv('randomstock100.csv', index=False)

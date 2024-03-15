import pandas as pd
import matplotlib.pyplot as plt

"""
read the data csv files into panda dataframes
"""
df_prices_0 = pd.read_csv('/home/nick/Projects/imc_prosperity/challenge_1/island-data-bottle-round-1/island-data-bottle-round-1/prices_round_1_day_0.csv', sep=';')
df_prices_1 = pd.read_csv('/home/nick/Projects/imc_prosperity/challenge_1/island-data-bottle-round-1/island-data-bottle-round-1/prices_round_1_day_-1.csv', sep=';')
df_prices_2 = pd.read_csv('/home/nick/Projects/imc_prosperity/challenge_1/island-data-bottle-round-1/island-data-bottle-round-1/prices_round_1_day_-2.csv', sep=';')
df_trades_0 = pd.read_csv('/home/nick/Projects/imc_prosperity/challenge_1/island-data-bottle-round-1/island-data-bottle-round-1/trades_round_1_day_0_nn.csv', sep=';')
df_trades_1 = pd.read_csv('/home/nick/Projects/imc_prosperity/challenge_1/island-data-bottle-round-1/island-data-bottle-round-1/trades_round_1_day_-1_nn.csv', sep=';')
df_trades_2 = pd.read_csv('/home/nick/Projects/imc_prosperity/challenge_1/island-data-bottle-round-1/island-data-bottle-round-1/trades_round_1_day_-2_nn.csv', sep=';')

"""
As i found out:
this step is not even necessary since we can check for equality for the object types in pandas
changes all the columns with object dtype to strings.
for prices:
product

for trades:
symbol, currency
"""
"""
df_trades_0['symbol'] = df_trades_0['symbol'].astype('|S80')
df_trades_1['symbol'] = df_trades_1['symbol'].astype('|S80')
df_trades_2['symbol'] = df_trades_2['symbol'].astype('|S80')
df_trades_0['currency'] = df_trades_0['currency'].astype('|S80')
df_trades_1['currency'] = df_trades_1['currency'].astype('|S80')
df_trades_2['currency'] = df_trades_2['currency'].astype('|S80')

df_prices_0['product'] = df_prices_0['product'].astype('|S80')
df_prices_1['product'] = df_prices_1['product'].astype('|S80')
df_prices_2['product'] = df_prices_2['product'].astype('|S80')
"""

"""
the first goal is to find a correlation between the bananas and the pearls

First constuct dataframes for both products

We have found no direct correlation between the two pairs
"""
df_midprice_0 = pd.DataFrame(index=range(20000),columns=['BANANAS', 'PEARLS'])
df_midprice_1 = pd.DataFrame(index=range(20000),columns=['BANANAS', 'PEARLS'])
df_midprice_2 = pd.DataFrame(index=range(20000),columns=['BANANAS', 'PEARLS'])

df_midprice_0['BANANAS'] = df_prices_0['mid_price'].loc[df_prices_0['product'] == 'BANANAS']
df_midprice_1['BANANAS'] = df_prices_1['mid_price'].loc[df_prices_1['product'] == 'BANANAS']
df_midprice_2['BANANAS'] = df_prices_2['mid_price'].loc[df_prices_2['product'] == 'BANANAS']
df_midprice_0['PEARLS'] = df_prices_0['mid_price'].loc[df_prices_0['product'] == 'PEARLS']
df_midprice_1['PEARLS'] = df_prices_1['mid_price'].loc[df_prices_1['product'] == 'PEARLS']
df_midprice_2['PEARLS'] = df_prices_2['mid_price'].loc[df_prices_2['product'] == 'PEARLS']


"""
here we want to check if there is a possible mean reverting strategie for the pearls
they always trade right around the 10'000 mark so we want to buy ich the ask price is below 10'000
and sell again when the bid price is above 10'000
"""

df_prices_0_pearls = df_prices_0.loc[df_prices_0['product'] == 'PEARLS']
df_prices_1_pearls = df_prices_1.loc[df_prices_1['product'] == 'PEARLS']
df_prices_2_pearls = df_prices_2.loc[df_prices_2['product'] == 'PEARLS']

"""
print('ask prices 0:')
print(df_prices_0_pearls['ask_price_1'].value_counts())
print('ask prices 1:')
print(df_prices_1_pearls['ask_price_1'].value_counts())
print('ask prices 2:')
print(df_prices_2_pearls['ask_price_1'].value_counts())

print('bid prices 0:')
print(df_prices_0_pearls['bid_price_1'].value_counts())
print('bid prices 1:')
print(df_prices_1_pearls['bid_price_1'].value_counts())
print('bid prices 2:')
print(df_prices_2_pearls['bid_price_1'].value_counts())
"""

"""
From these tests we have found a strategy for the PEARL product

Buy if the best ask price is currently at 9998 and then sell again if the best bid is at 10002
this should happen around 800 times during a day
in this strategy it is best to always have buy and sell orders at the given prices so we don't have to deal
with latency issues
"""

"""
for the bananas product we try fo take advantage of order book inbalances to determin the trend of the stock
resources from https://dm13450.github.io/2022/02/02/Order-Flow-Imbalance.html
"""


"""
i want to analyze the moving average of the midprice of the bananas.
maybe we can creat a mean reverting strategy
"""

df_midprice_bananas_0 = pd.DataFrame(columns=['Time', 'Midprice'])
df_midprice_bananas_0['Time'] = df_prices_0['timestamp'].loc[df_prices_0['product'] == 'BANANAS']
df_midprice_bananas_0['Midprice'] = df_prices_0['mid_price'].loc[df_prices_0['product'] == 'BANANAS']
df_midprice_bananas_1 = pd.DataFrame(columns=['Time', 'Midprice'])
df_midprice_bananas_1['Time'] = df_prices_1['timestamp'].loc[df_prices_1['product'] == 'BANANAS']
df_midprice_bananas_1['Midprice'] = df_prices_1['mid_price'].loc[df_prices_1['product'] == 'BANANAS']
df_midprice_bananas_2 = pd.DataFrame(columns=['Time', 'Midprice'])
df_midprice_bananas_2['Time'] = df_prices_2['timestamp'].loc[df_prices_2['product'] == 'BANANAS']
df_midprice_bananas_2['Midprice'] = df_prices_2['mid_price'].loc[df_prices_2['product'] == 'BANANAS']

df_midprice_bananas_0['MA'] = df_midprice_bananas_0['Midprice'].rolling(window=20).mean()
df_midprice_bananas_0['Spread'] = df_midprice_bananas_0['Midprice']-df_midprice_bananas_0['MA']


df_prices_0_bananas = df_prices_0.loc[df_prices_0['product'] == 'BANANAS']
df_prices_1_bananas = df_prices_1.loc[df_prices_1['product'] == 'BANANAS']
df_prices_2_bananas = df_prices_2.loc[df_prices_2['product'] == 'BANANAS']

df_prices_0_bananas['MA'] = df_prices_0_bananas['mid_price'].rolling(window=20).mean()
df_prices_1_bananas['MA'] = df_prices_1_bananas['mid_price'].rolling(window=20).mean()
df_prices_2_bananas['MA'] = df_prices_2_bananas['mid_price'].rolling(window=20).mean()

df_prices_0_bananas['ask_ma_spread'] = df_prices_0_bananas['ask_price_1'] - df_prices_0_bananas['MA']
df_prices_0_bananas['bid_ma_spread'] = df_prices_0_bananas['bid_price_1'] - df_prices_0_bananas['MA']

df_prices_1_bananas['ask_ma_spread'] = df_prices_1_bananas['ask_price_1'] - df_prices_1_bananas['MA']
df_prices_1_bananas['bid_ma_spread'] = df_prices_1_bananas['bid_price_1'] - df_prices_1_bananas['MA']

df_prices_2_bananas['ask_ma_spread'] = df_prices_2_bananas['ask_price_1'] - df_prices_2_bananas['MA']
df_prices_2_bananas['bid_ma_spread'] = df_prices_2_bananas['bid_price_1'] - df_prices_2_bananas['MA']




df_prices_2_bananas.plot(y=['ask_ma_spread', 'bid_ma_spread'], x='timestamp')
# plt.show()

df_prices_2_bananas.plot(y=['mid_price', 'ask_price_1', 'bid_price_1', 'MA'],x='timestamp')
plt.show()



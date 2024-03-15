import pandas as pd
import numpy as np
import scipy
import matplotlib.pyplot as plt

import statsmodels
import statsmodels.api as sm
from statsmodels.tsa.stattools import coint, adfuller   

df_prices_m1 = pd.read_csv('/home/nick/Projects/imc_prosperity/challenge_2/island-data-bottle-round-2/island-data-bottle-round-2/prices_round_2_day_-1.csv', sep=';')
df_prices_0 = pd.read_csv('/home/nick/Projects/imc_prosperity/challenge_2/island-data-bottle-round-2/island-data-bottle-round-2/prices_round_2_day_0.csv', sep=';')
df_prices_1 = pd.read_csv('/home/nick/Projects/imc_prosperity/challenge_2/island-data-bottle-round-2/island-data-bottle-round-2/prices_round_2_day_1.csv', sep=';')
df_trades_m1 = pd.read_csv('/home/nick/Projects/imc_prosperity/challenge_2/island-data-bottle-round-2/island-data-bottle-round-2/trades_round_2_day_-1_nn.csv', sep=';')
df_trades_0 = pd.read_csv('/home/nick/Projects/imc_prosperity/challenge_2/island-data-bottle-round-2/island-data-bottle-round-2/trades_round_2_day_0_nn.csv', sep=';')
df_trades_1 = pd.read_csv('/home/nick/Projects/imc_prosperity/challenge_2/island-data-bottle-round-2/island-data-bottle-round-2/trades_round_2_day_1_nn.csv', sep=';')

"""
so in this round we have two new products: Coconuts and Pinacoladas
coconuts: around 8'000 seashells
pinacoladas: around 15'000 seashells

no pinacoladas without coconuts but coconuts without pinacoladas

so the first strategy in mind is that of a simple pairs trading strategy
if the price of the coconuts changes so should the price of the pinacoladas
"""

"""
we first start by analyzing the spread between the coconuts price and the 
"""
df_prices_m1_coconuts = df_prices_m1.loc[df_prices_m1['product'] == 'COCONUTS']
df_prices_0_coconuts = df_prices_0.loc[df_prices_0['product'] == 'COCONUTS']
df_prices_1_coconuts = df_prices_1.loc[df_prices_1['product'] == 'COCONUTS']
df_prices_m1_pina_coladas = df_prices_m1.loc[df_prices_m1['product'] == 'PINA_COLADAS']
df_prices_0_pina_coladas = df_prices_0.loc[df_prices_0['product'] == 'PINA_COLADAS']
df_prices_1_pina_coladas = df_prices_1.loc[df_prices_1['product'] == 'PINA_COLADAS']

df_prices_m1_coconuts = df_prices_m1_coconuts.set_index('timestamp')
df_prices_0_coconuts = df_prices_0_coconuts.set_index('timestamp')
df_prices_1_coconuts = df_prices_1_coconuts.set_index('timestamp')

df_prices_m1_pina_coladas = df_prices_m1_pina_coladas.set_index('timestamp')
df_prices_0_pina_coladas = df_prices_0_pina_coladas.set_index('timestamp')
df_prices_1_pina_coladas = df_prices_1_pina_coladas.set_index('timestamp')


df_spread_m1 = (df_prices_m1_coconuts['ask_price_1']) - (df_prices_m1_pina_coladas['bid_price_1'] - 7008)
df_spread_0 = (df_prices_0_coconuts['ask_price_1']) - (df_prices_0_pina_coladas['bid_price_1'] - 7008)
df_spread_1 = (df_prices_1_coconuts['ask_price_1']) - (df_prices_1_pina_coladas['bid_price_1'] - 7008)

# df_spread_m1.plot(kind='kde', legend='-1', color='b')   
# df_spread_0.plot(kind='kde', legend='0', color='g')
# df_spread_1.plot(kind='kde', legend='1', color='r')

# plt.show()


df_spread_0.index += 1000000
df_spread_1.index += 2000000

df_spread_complete = df_spread_m1.append(df_spread_0)
df_spread_complete = df_spread_complete.append(df_spread_1)

df_spread_complete.plot()


pvalue = adfuller(df_spread_complete)[1]
print('p value: ', pvalue)
print(df_spread_complete.mean())
plt.show()

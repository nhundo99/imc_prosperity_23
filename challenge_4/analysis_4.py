import pandas as pd
import numpy as np
import scipy
import matplotlib.pyplot as plt

import statsmodels
import statsmodels.api as sm
from statsmodels.tsa.stattools import coint, adfuller 

"""
inventory of PICNIC_BASKET:
2 BAGUETTE
4 DIP
1 UKULELE
"""

df_prices_1 = pd.read_csv('/home/nick/Projects/imc_prosperity/challenge_4/island-data-bottle-round-4/island-data-bottle-round-4/prices_round_4_day_1.csv', sep=';')
df_prices_2 = pd.read_csv('/home/nick/Projects/imc_prosperity/challenge_4/island-data-bottle-round-4/island-data-bottle-round-4/prices_round_4_day_2.csv', sep=';')
df_prices_3 = pd.read_csv('/home/nick/Projects/imc_prosperity/challenge_4/island-data-bottle-round-4/island-data-bottle-round-4/prices_round_4_day_3.csv', sep=';')
df_trades_1 = pd.read_csv('/home/nick/Projects/imc_prosperity/challenge_4/island-data-bottle-round-4/island-data-bottle-round-4/trades_round_4_day_1_nn.csv', sep=';')
df_trades_2 = pd.read_csv('/home/nick/Projects/imc_prosperity/challenge_4/island-data-bottle-round-4/island-data-bottle-round-4/trades_round_4_day_2_nn.csv', sep=';')
df_trades_3 = pd.read_csv('/home/nick/Projects/imc_prosperity/challenge_4/island-data-bottle-round-4/island-data-bottle-round-4/trades_round_4_day_3_nn.csv', sep=';')

"""
new column where we price the 3 components together in a basket
so that we can compare it to the actual basket price
"""

df_prices_1 = df_prices_1.set_index('timestamp')

df_prices_2 = df_prices_2.set_index('timestamp')
df_prices_2.index += 1000000

df_prices_3 = df_prices_3.set_index('timestamp')
df_prices_3.index += 2000000


df_prices_complete = pd.concat([df_prices_1, df_prices_2, df_prices_3])


df_prices_dip = df_prices_complete.loc[df_prices_complete['product'] == 'DIP']
df_prices_baguette = df_prices_complete.loc[df_prices_complete['product'] == 'BAGUETTE']
df_prices_ukulele = df_prices_complete.loc[df_prices_complete['product'] == 'UKULELE']

df_prices_components = pd.DataFrame(columns=['midprice'])
df_prices_components['midprice'] = 2*df_prices_baguette['mid_price'] + 4*df_prices_dip['mid_price'] + df_prices_ukulele['mid_price']

df_prices_basekt = df_prices_complete.loc[df_prices_complete['product'] == 'PICNIC_BASKET']



df_spread = df_prices_basekt['mid_price'] - df_prices_components['midprice']
mean_spread = df_spread.mean()
std_spread = df_spread.std()
print(mean_spread)
print(std_spread)
df_spread.plot()
plt.show()
"""
# df_prices_complete['components_combined'] = pd.concat([df_prices_1['components_combined'], df_prices_2['components_combined'], df_prices_3['components_combined']])

print(df_prices_complete)
print(df_prices_1)
print(df_prices_2)
"""

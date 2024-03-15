import pandas as pd
import numpy as np
import scipy
import matplotlib.pyplot as plt

import statsmodels
import statsmodels.api as sm
from statsmodels.tsa.stattools import coint, adfuller   

df_prices_0 = pd.read_csv('/home/nick/Projects/imc_prosperity/challenge_3/island-data-bottle-round-3/island-data-bottle-round-3/prices_round_3_day_0.csv', sep=';')
df_prices_1 = pd.read_csv('/home/nick/Projects/imc_prosperity/challenge_3/island-data-bottle-round-3/island-data-bottle-round-3/prices_round_3_day_1.csv', sep=';')
df_prices_2 = pd.read_csv('/home/nick/Projects/imc_prosperity/challenge_3/island-data-bottle-round-3/island-data-bottle-round-3/prices_round_3_day_2.csv', sep=';')
df_trades_0 = pd.read_csv('/home/nick/Projects/imc_prosperity/challenge_3/island-data-bottle-round-3/island-data-bottle-round-3/trades_round_3_day_0_nn.csv', sep=';')
df_trades_1 = pd.read_csv('/home/nick/Projects/imc_prosperity/challenge_3/island-data-bottle-round-3/island-data-bottle-round-3/trades_round_3_day_1_nn.csv', sep=';')
df_trades_2 = pd.read_csv('/home/nick/Projects/imc_prosperity/challenge_3/island-data-bottle-round-3/island-data-bottle-round-3/trades_round_3_day_2_nn.csv', sep=';')


df_prices_0_diving_gear = df_prices_0.loc[df_prices_0['product'] == 'DIVING_GEAR']
df_prices_1_diving_gear = df_prices_1.loc[df_prices_1['product'] == 'DIVING_GEAR']
df_prices_2_diving_gear = df_prices_2.loc[df_prices_2['product'] == 'DIVING_GEAR']
df_prices_0_diving_gear = df_prices_0_diving_gear.set_index('timestamp') 
df_prices_1_diving_gear = df_prices_1_diving_gear.set_index('timestamp') 
df_prices_2_diving_gear = df_prices_2_diving_gear.set_index('timestamp') 
df_prices_1_diving_gear.index += 1000000
df_prices_2_diving_gear.index += 2000000
df_prices_complete_diving_gear = pd.concat([df_prices_0_diving_gear, df_prices_1_diving_gear, df_prices_2_diving_gear])



df_prices_0_berries = df_prices_0.loc[df_prices_0['product'] == 'BERRIES']
df_prices_1_berries = df_prices_1.loc[df_prices_1['product'] == 'BERRIES']
df_prices_2_berries = df_prices_2.loc[df_prices_2['product'] == 'BERRIES']
df_prices_0_berries = df_prices_0_berries.set_index('timestamp')
df_prices_1_berries = df_prices_1_berries.set_index('timestamp')
df_prices_2_berries = df_prices_2_berries.set_index('timestamp')
df_prices_1_berries.index += 1000000
df_prices_2_berries.index += 2000000
df_prices_complete_berries = pd.concat([df_prices_0_berries, df_prices_1_berries, df_prices_2_berries])
df_prices_complete_berries['MA'] = df_prices_complete_berries['mid_price'].rolling(800).mean()


df_prices_0_dolphin_sightings = df_prices_0.loc[df_prices_0['product'] == 'DOLPHIN_SIGHTINGS']
df_prices_1_dolphin_sightings = df_prices_1.loc[df_prices_1['product'] == 'DOLPHIN_SIGHTINGS']
df_prices_2_dolphin_sightings = df_prices_2.loc[df_prices_2['product'] == 'DOLPHIN_SIGHTINGS']
df_prices_0_dolphin_sightings = df_prices_0_dolphin_sightings.set_index('timestamp')
df_prices_1_dolphin_sightings = df_prices_1_dolphin_sightings.set_index('timestamp')
df_prices_2_dolphin_sightings = df_prices_2_dolphin_sightings.set_index('timestamp')
df_prices_1_dolphin_sightings.index += 1000000
df_prices_2_dolphin_sightings.index += 2000000
df_prices_complete_dolphin_sightings = pd.concat([df_prices_0_dolphin_sightings, df_prices_1_dolphin_sightings, df_prices_2_dolphin_sightings])

df_prices_complete_dolphin_sightings['trend'] = 3010+(0.000031*df_prices_complete_dolphin_sightings.index)
df_prices_complete_dolphin_sightings['change'] = df_prices_complete_dolphin_sightings['mid_price'] - df_prices_complete_dolphin_sightings['mid_price'].shift(1)
df_prices_complete_dolphin_sightings['rolling_change'] = df_prices_complete_dolphin_sightings['change'].rolling(5).sum()
"""
tested with 20 rolling: only 3 real oppurtunities over the entiiere data but seems promissing

If we have time it might be useful to test if there is something special if the change
in sightings is much higher at one point than the current rolling sum or average of sightings
or rolling sum or average in the change in sightings
"""

df_ratio = df_prices_complete_diving_gear['mid_price']/df_prices_complete_dolphin_sightings['mid_price']

print(df_prices_complete_dolphin_sightings)
# ax = df_prices_complete_dolphin_sightings.plot(y='mid_price', figsize=(8,8))
# df_prices_complete_diving_gear.plot(ax=ax, y='mid_price')

df_ratio.plot()
ax = df_prices_complete_dolphin_sightings.plot(y='trend', figsize=(8,8))
df_prices_complete_diving_gear.plot(y='mid_price')
df_prices_complete_dolphin_sightings.plot(ax=ax, y='mid_price')
df_prices_complete_dolphin_sightings.plot(y='rolling_change')

plt.show()


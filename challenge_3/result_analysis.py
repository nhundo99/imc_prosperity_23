import pandas as pd
import numpy as np
import scipy
import matplotlib.pyplot as plt

import statsmodels
import statsmodels.api as sm
from statsmodels.tsa.stattools import coint, adfuller 

df_results_3 = pd.read_csv('/home/nick/Projects/imc_prosperity/challenge_3/results_3.csv', sep=';')

df_results_3.loc[df_results_3['product'] == 'BERRIES'].plot(x='timestamp', y='mid_price')
plt.show()
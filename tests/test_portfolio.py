import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json

import sys
sys.path.append('../src/bigbucks_port')
import portfolio

from bigbucks_db import *

# # Example data
# er = np.array([.05, .04, .03])
# sd = np.array([.2, .1, .05])
# corr = [[1,.5,0],
#         [.5,1,.5],
#         [0,.5,1]]
# covar = np.diag(sd) @ corr @ np.diag(sd)

objs_realtime = Buy_And_Sell(STOCK_API_KEYS)
objs = Table_View(url, key)

# returns,risk = portfolio.frontier(objs,8,100)
# plt.scatter(risk,returns)
# plt.show()
# print(portfolio.frontier_json(objs,8,100))
print(portfolio.frontier_json(objs,3,10))
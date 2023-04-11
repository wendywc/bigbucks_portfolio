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

url = "https://lhjpufbcymwhprgzfbwt.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxoanB1ZmJjeW13aHByZ3pmYnd0Iiwicm9sZSI6ImFub24iLCJpYXQiOjE2Nzk2MDY3MDMsImV4cCI6MTk5NTE4MjcwM30.42A0qtrLYChbrdUzjf1E7TRgHionW5xrZRK-e9wBqPk"
STOCK_API_KEYS = "9Q91BWGMOE13WOR3"

objs_realtime = Buy_And_Sell(STOCK_API_KEYS)
objs = Table_View(url, key)

print(portfolio.frontier_json(objs,6,5))
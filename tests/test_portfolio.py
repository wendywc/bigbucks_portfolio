import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json

import sys
sys.path.append('../src/bigbucks_port')
import portfolio

from bigbucks_db import *

# Example data
er = np.array([.05, .04, .03])
sd = np.array([.2, .1, .05])
corr = [[1,.5,0],
        [.5,1,.5],
        [0,.5,1]]
covar = np.diag(sd) @ corr @ np.diag(sd)

# means, stds = portfolio.frontier(objs,6,100)
# plt.scatter(stds, means)
# plt.show()
# print(portfolio.frontier_json(objs,None,3))
# js = portfolio.return_json(objs,6)
# print(json.loads(js)[0])
# print(portfolio.spy_json(objs))
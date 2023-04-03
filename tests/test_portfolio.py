import pandas as pd
import numpy as np

# Example data
er = np.array([.05, .04, .03])
sd = np.array([.2, .1, .05])
corr = [[1,.5,0],
        [.5,1,.5],
        [0,.5,1]]
covar = np.diag(sd) @ corr @ np.diag(sd)


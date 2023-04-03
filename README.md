## Introduction

This package is used for portfolio analysis in FINTECH 512 Bigbucks project. This package also depends on the `bigbucks_db` package to interact with the supabase database and Alpha Vantage. 

## Connect to supabase and alpha Vantage
```python
# Connect to supabase
SUPABASE_URL = ""
KEYS = ""
objs = Table_View(SUPABASE_URL, KEYS)

# Connect to Alpha Vantage
STOCK_API_KEYS = ""
objs_realtime = Buy_And_Sell(STOCK_API_KEYS)
```
Import package
```python
from bigbucks_port.portfolio import *
```

## Functions
- Get the current portfolio holdings for user. 
It returns a json list includes the stock symbol, number of shares and price per share (weighted by historical cost)
Note: If you want to get all the stocks for all the users, set `id=None`. Same for other functions below. 

```python
holding = current_holding(objs,6)
```
Example output:
```python
[{"stock_symbol":"AAPL","num_shares":0,"pv":0.0,"price per share":null},{"stock_symbol":"IBM","num_shares":100,"pv":13107.0007324219,"price per share":131.0700073242}]
```

- Calculate the expected return, std and covariance of portfolio
The statistics are calculated based on the historical data. 
Note: It returns 4 values, the fourth one is the json list with expected return and std for each stock and the rest 3 are used in later functions.

```python
er,std,covar,er_std_json = er_covar(objs,6)
```
Example output of `er_std_json`
```python
{"mean":{"AAPL":0.2318697889,"IBM":-0.0075799068},"std":{"AAPL":0.3361717704,"IBM":0.2759977582}}
```

- Get the risk and return for a list of portfolios with randomly generated weights

```python
# N: number of portfolios generated
return_risk = rand_scatter(5,objs,6)
```
Example output
```python
{"mean": [0.13009300157209497, 0.02497749995225248, 0.16554410436129516, 0.14454572030763208, 0.10086096141188186], "std": [0.06705431545265916, 0.0656856601122741, 0.07160084144613905, 0.0686922284906061, 0.06474888518469718]}
```

- Get the risk and return for the efficient frontier
```python
return_risk = frontier(objs,6)
```
Example output
```python
{"mean": [],"std":[]}
```

- Get the optimal portfolio given a risk free rate

```python
opt = optimize_port(0.0025,objs,6)
```
Example output
```python
{"opt mean": 0.2318697888966346, "opt std": 0.08412521675427394, "opt sharpe": 2.7265283555418782}
```

- Get the risk and return for the current portfolio
Note: weight is calculated by the current holding

```python
risk_return = cur_risk_return(0.0025,objs,6)
```
Example output
```python
{'mean': -0.007579906778486523, 'std': 0.06906698680510652, 'sharpe': -0.1459439197330273}
```

- Calculate the holding period return and balance
```python
holding_stat = holding_return(objs,6,objs_realtime)
```

Example output
```python
# PV: the market value of all cash and stocks in the account
# Cash: cash remained in the account balance
{'PV': 1000000.0, 'Cash': 986892.9992675781, 'Holding period return': 0.0}
```


# bigbucks_portfolio
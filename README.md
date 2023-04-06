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
### Get the current portfolio holdings for user. 
- It returns a json list includes the stock symbol, number of shares, historical cost and price per share.
- If you want to get all the stocks for all the users, set `id=None`. Same for other functions below. 

```python
id =6
holding = holding_json(objs,id)
```
Example output:
```python
{"IBM":{"num_shares":100,"historical_cost":13107.0007324219,"price_per_share":131.0700073242}}
```
### Calculate the historical daily return for each stock in the holding 
```python
returns = return_json(objs,id)
```
Example output:
```python
[{"Symbol": "AAPL", "labels": ["2018-04-03", "2018-04-04"], "data": [{"date": "2018-04-03", "return": 0.010206911067964735}, {"date": "2018-04-04", "return": 0.01894174279199366}]}, {"Symbol": "IBM", "labels": ["2018-04-03", "2018-04-04"], "data": [{"date": "2018-04-03", "return": -0.0014670581452283652}, {"date": "2018-04-04", "return": 0.028096725995288337}]}]
```
### Calculate the historical daily return for SPY 
```python
returns = spy_json(objs)
```

Example output:
```python
{"Symbol": "SPY", "labels": ["2018-04-10", "2018-04-11"], "data": [{"date": "2018-04-10", "return": 0.016588598996312102}, {"date": "2018-04-11", "return": -0.005540685772461173}]}
```

### Calculate the expected return and std of each stock in the portfolio
- It returns a a json list of mean and std for each stock
```python
er_std = er_std_json(obj,id)
```
Example output:
```python
{"AAPL":{"mean":0.2318697889,"std":0.3361717704},"IBM":{"mean":-0.0075799068,"std":0.2759977582}}
```

### Get the risk and return for the efficient frontier
- 
```python
# num: number of portfolios on the efficient frontier
return_risk = frontier_json(objs,id,num)
```
Example output
```python
{"data": [{"std": 0.06906698680510652, "mean": -0.007579906778486523}, {"std": 0.06906698680510652, "mean": -0.007579906778486523}]}
```

### Get the optimal portfolio given a risk free rate

```python
# rf: risk free rate
opt = optimize_port(rf,objs,id)
```
Example output
```python
{"opt mean": 0.2318697888966346, "opt std": 0.08412521675427394, "opt sharpe": 2.7265283555418782}
```

### Calculate the risk, return and sharpe for the current holding

```python
risk_return = cur_risk_return(0.0025,objs,6)
```
Example output
```python
{'mean': -0.007579906778486523, 'std': 0.06906698680510652, 'sharpe': -0.1459439197330273}
```

### Calculate the holding period return and cash balance
```python
holding_stat = holding_return(objs,6,objs_realtime)
```

Example output
```python
# PV: the market value of all cash and stocks in the account
# Cash: cash remained in the account balance
{'PV': 1000106.999206543, 'Cash': 986892.9992675781, 'Holding_return': 0.00010699920654300143}
```

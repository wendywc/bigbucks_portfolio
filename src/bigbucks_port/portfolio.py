import numpy as np
from math import sqrt
import json
# Check if all packages installed 
try:
    import pandas as pd
except ImportError as e:
    print("Package <pandas> needed to be installed before getting data ! ")
    raise e
try:
    from scipy.optimize import minimize
except ImportError as e:
    print("Package <scipy> needed to be installed before getting data ! ")
    raise e
try:
    from bigbucks_db import *
except ImportError as e:
    print("Package <bigbucks-db> needed to be installed before getting data ! ")
    raise e

# Ignore warnings
import warnings
warnings.simplefilter('ignore')

# Get the portfolio holdings for each customer
def current_holding(objs,id):
    # all the transactions 
    trans_all = pd.json_normalize(objs.view_table_data("Transaction_Records"))
    # ID=none, use all the stocks
    if id == None:
        trans = trans_all
    else:
        # The transaction for this customer
        trans = trans_all[trans_all["customer_id"]==id]
    # assign signal for numbers buy+,sell-
    trans["num_shares"]=trans.apply(lambda x: x["num_shares"] if x["condition"] == "buy" else -x["num_shares"],axis=1)
    trans["pv"] = trans.apply(lambda x: x["num_shares"]*x["stock_price_realtime"],axis=1)
    # Group by symbol
    holding = trans[['stock_symbol','num_shares','pv']].groupby('stock_symbol').sum()
    # Calculate the actual price per share
    holding['price per share'] = holding['pv']/holding['num_shares']
    # Convert to json
    holding.reset_index(inplace=True)
    holding = holding.to_json(orient='records')
    return holding

# Calculate the daily returns for the stocks in the portfolio
def cal_returns(objs,id):
    # Get the symbols in the holding
    holdings = current_holding(objs,id)
    symbols = pd.json_normalize(json.loads(holdings))['stock_symbol'].to_numpy()
    stockreturns = pd.DataFrame(columns=symbols)
    # Get the daily prices for the given symbol
    for s in symbols:
        stockprice = pd.json_normalize(objs.view_symbol_price_data(s))
        # Sort prices by date
        stockprice.sort_values(by='date',inplace=True)
        # calculate the daily returns
        returns = np.log(stockprice['adjusted_close']/stockprice['adjusted_close'].shift(1))
        stockreturns[s]=returns.to_numpy()
    stockreturns.dropna(inplace=True)
    return stockreturns

# Calculate the expected return, std and covariance
def er_covar(objs,id):
    stockreturns = cal_returns(objs,id)
    t = stockreturns.shape[0]
    # Expected return and annualize
    er = ((stockreturns+1).prod()**(1/t)-1)*255
    # standard deviation and annualize
    std = stockreturns.std()*sqrt(255)
    # covariance and annualize
    covar = stockreturns.cov()*sqrt(255)
    # convert er and std to json format
    er_std = pd.concat([er,std],axis=1)
    er_std.columns=["mean","std"]
    er_std_json = er_std.to_json()
    return er,std,covar,er_std_json

# Generate random weights for scatter plots
# Helper function
def rand_weights(n):
    ''' Produces n random weights that sum to 1 '''
    k = np.random.rand(n)
    return k / sum(k)

# Helper function
def rand_port(er,covar):
    # number of assets in portfolio
    n = er.size
    w = rand_weights(n)
    # portfolio return
    mu = (w @ er.reshape(-1,1))[0]
    # portfolio std
    std = sqrt(w @ covar @ w.reshape(-1,1))
    return mu,std

# randomly generated portfolios
def rand_scatter(N,objs,id):
    er = er_covar(objs,id)[0].to_numpy()
    covar = er_covar(objs,id)[2].to_numpy()
    means, stds = np.column_stack([rand_port(er,covar) for _ in range(N)])
    # convert to json format
    return_risk = {'mean':means.tolist(),'std':stds.tolist()}
    return_risk_js = json.dumps(return_risk)
    return return_risk_js

# calculate the minimum std given a return
# Helper function
def min_risk(R,er,covar,n):
    def risk_cal(w):
        std = sqrt(w.T @ covar @ w)
        return std
    w0 = np.array([1/n]*n).reshape(-1,1)
    w_min = minimize(risk_cal,w0,
                    constraints=({'type':'ineq','fun': lambda x: x},{'type':'ineq','fun': lambda x: 1-x},{'type':'eq','fun': lambda x:x.sum()-1},{'type':'eq','fun': lambda x: x.T @ er.reshape(-1,1)-R}))
    std_min = sqrt(w_min.x @ covar @ w_min.x.reshape(-1,1))
    return std_min

# Calculate the risk and return for efficient frontier
def frontier(objs,id):
    er = er_covar(objs,id)[0].to_numpy()
    covar = er_covar(objs,id)[2].to_numpy()
    #number of assets
    n=len(er)
    r_min = er.min()
    r_max = er.max()
    returns = np.linspace(r_min,r_max,num=100)
    risk = np.array([min_risk(r,er,covar,n) for r in returns])
    # convert to json format
    return_risk = {'mean':returns.tolist(),'std':risk.tolist()}
    return_risk_js = json.dumps(return_risk)
    return return_risk_js
    
# optimal portfolio with max sharpe
def optimize_port(rf,objs,id):
    er = er_covar(objs,id)[0].to_numpy()
    covar = er_covar(objs,id)[2].to_numpy()
    n = len(er)
    def sharpe_cal(w):
        r = w.T @ er.reshape(-1,1)
        std = sqrt(w.T @ covar @ w)
        sharpe = (r-rf)/std
        return -sharpe
    #Initial weights
    w0 = np.array([1/n]*n).reshape(-1,1)
    w_optmize = minimize(sharpe_cal,w0,
                         constraints=({'type':'ineq','fun': lambda x: x},{'type':'ineq','fun': lambda x: 1-x},{'type':'eq','fun': lambda x:x.sum()-1}))
    # Optimal values
    er_max = (w_optmize.x @ er.reshape(-1,1))[0]
    std_min = sqrt(w_optmize.x @ covar @ w_optmize.x.reshape(-1,1))
    sharpe = -w_optmize.fun
    # Convert to json
    opt = {"opt mean":er_max,"opt std":std_min,"opt sharpe":sharpe}
    opt_js = json.dumps(opt)
    return opt_js

# get the return and risk for the current holding
def cur_risk_return(rf,objs,id):
    er = er_covar(objs,id)[0].to_numpy()
    covar = er_covar(objs,id)[2].to_numpy()
    # Get the current holding
    holdings = current_holding(objs,id)
    holdings_df = pd.json_normalize(json.loads(holdings))
    # Get the current weight
    weight = (holdings_df['pv']/holdings_df['pv'].sum()).to_numpy()
    # Calculate the current risk and return 
    mean = (weight @ er.reshape(-1,1))[0]
    std = sqrt(weight @ covar @ weight.reshape(-1,1))
    sharpe = (mean-rf)/std
    # Convert to json
    current = {"mean":mean,"std":std,"sharpe":sharpe}
    return current

# get the holding period return
def holding_return(objs,id,objs_realtime):
    holdings = current_holding(objs,id)
    holdings_df = pd.json_normalize(json.loads(holdings))
    holdings_df['price now'] = holdings_df['stock_symbol'].apply(lambda x: objs_realtime.get_realtime_stock_price(x))
    # Current cash balance
    cash = 1000000 - holdings_df['pv'].sum()
    # present value of stocks
    pv_stock = (holdings_df['price now']*holdings_df['num_shares']).sum()
    # PV
    PV = cash+pv_stock
    # Holding period return
    r = PV/1000000-1
    # return json format
    holding_stat = {"PV":PV,"Cash":cash,"Holding period return":r}
    return holding_stat
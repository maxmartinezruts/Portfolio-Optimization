"""
Author: Max Martinez Ruts
Date: October 2019
Idea:

Find an optimum porfolio by using a numerical method to simply try setting random weights and testing beta-return for each
combination of weights. Then selecting the beta-return point that leads to the highest return-beta slope (optimum portfolio)
"""


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Import data from several stock markets
stocks = []
stocks.append(pd.read_csv("DJI.csv")[-4000:])
stocks.append(pd.read_csv("GSPC.csv")[-4000:])
stocks.append(pd.read_csv("AAPL.csv")[-4000:])
stocks.append(pd.read_csv("MSI.csv")[-4000:])
stocks.append(pd.read_csv("MSFT.csv")[-4000:])
# stocks.append(pd.read_csv("GOOG.csv")[-4000:])

Rf = 1.00019942227



opens = []
closes = []
returns = []
rates = []

# Store relevant data
for stock in stocks:
    opens.append(np.array(stock['Open']))
    closes.append(np.array(stock['Close']))
    returns.append(closes[-1]/opens[-1])
    rates.append(closes[-1] / opens[-1])

# Create time array ranging from 0 to the last opening
ts = np.arange(0,len(opens[0]),1)

# Create the covariance matrix
mat = rates
cov = np.cov(mat)
corr = np.corrcoef(mat)
expret = np.mean(rates, axis=1)

print(expret)
ps = []

for i in range(len(stocks)):
    ps.append([np.sqrt(cov[i,i]),expret[i]])

xs = []
ys = []
max_slope = 0

X = 1000

# Repeat X times
for i in range(X):
    for j in range(len(stocks)):

        # Associate random weights
        ws = np.random.uniform(0,10,(len(stocks),1))
        ws = ws/np.sum(ws)

        # Determine the return and risk using such weights
        weighted_cov = np.sqrt(np.sum(np.matmul(ws, ws.transpose())* cov))
        weighted_ret = np.sum(np.dot(expret, ws))

        # Get return to beta slope
        slope = (weighted_ret-Rf)/weighted_cov


        # If the point found is better than any other found yet, update max
        if slope > max_slope:
            max_slope = slope
            max_point = [weighted_cov, weighted_ret]

        # Append to the list to plot them later
        xs.append(weighted_cov)
        ys.append(weighted_ret)
        # print('Weight:',w1, 'Risk:',weighted_cov, 'Return:',weighted_ret)

# Plot the points (each point represents a beta-return possible by using its associated weights)
plt.scatter(xs, ys)

# Plot important points and slope
plt.scatter([p[0] for p in ps], [p[1] for p in ps])
plt.scatter(max_point[0], max_point[1])
plt.scatter(0, Rf)

plt.show()


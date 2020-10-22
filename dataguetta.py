import yfinance as yf
import pandas as pd
import numpy as np
import sys

if len(sys.argv) <= 1:
    exit("Too less arguments calling script usage: dataguetta.py STOCK interval (see yfinance)")
elif len(sys.argv) != 3:
    exit("usage: dataguetta.py STOCK interval (see yfinance)")

STOCK = sys.argv[1]
INT = sys.argv[2]
# specify according to needs
period = "1y"
if "h" in INT:
    period = "720d"
elif "5m" in INT:
    period = "60d"
elif "1m" in INT:
    period = "7d"
data = yf.download(STOCK,period=period,interval=INT)

a = int(len(data) * 0.9)
train = data[:a]
test = data[a:]

#i need
# Date,Open,High,Low,Close,Close,Volume
# 2010-08-12,17.799999,17.900000,17.389999,17.600000,17.600000,691000

data.to_csv("data/%s_%s_all.csv.gz"%(STOCK,INT),compression="gzip")
train.to_csv("data/%s_%s_train.csv.gz"%(STOCK,INT),compression="gzip")
test.to_csv("data/%s_%s_test.csv.gz"%(STOCK,INT),compression="gzip")

print(train.head())
print(train.shape,data.shape)
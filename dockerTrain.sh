#!/bin/bash
# add what you want to train simulataneaously
exec python train.py data/BTCUSD\=X_1d_train.csv data/BTCUSD\=X_1d_test.csv --model-name btcusd1d --episode-count 200 &
exec python train.py data/AAPL_1d_all.csv data/AAPL_test.csv --model-name aapl1d --episode-count 200
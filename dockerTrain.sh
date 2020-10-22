#!/bin/bash
# add what you want to train simulataneaously
exec ls data/ & 
exec python train.py "data/BTCUSD=X_1d_train.csv.gz" "data/BTCUSD=X_1d_test.csv.gz" --model-name btcusd1d --episode-count 200 &
exec python train.py "data/AAPL_1d_train.csv.gz" "data/AAPL_1d_test.csv.gz" --model-name aapl1d --episode-count 200
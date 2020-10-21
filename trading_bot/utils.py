import joblib
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import os
#import tensorflow as tf


# Formats Position
format_position = lambda price: ('-$' if price < 0 else '+$') + '{0:.2f}'.format(abs(price))


# Formats Currency
format_currency = lambda price: '${0:.2f}'.format(abs(price))

def show_train_result(result, val_position, initial_offset):
    """ Displays training results
    """
    if val_position == initial_offset or val_position == 0.0:
        print('Episode {}/{} - Train Position: {}  Val Position: USELESS  Train Loss: {:.4f}'
                     .format(result[0], result[1], format_position(result[2]), result[3]))
    else:
        print('Episode {}/{} - Train Position: {}  Val Position: {}  Train Loss: {:.4f})'
                     .format(result[0], result[1], format_position(result[2]), format_position(val_position), result[3],))


def show_eval_result(model_name, profit, initial_offset):
    """ Displays eval results
    """
    if profit == initial_offset or profit == 0.0:
        print('{}: USELESS\n'.format(model_name))
    else:
        print('{}: {}\n'.format(model_name, format_position(profit)))


def get_stock_data(stock_file):
    """Reads stock data from csv file
    """
    # Datetime = Date if non hourly
    try:
        df = pd.read_csv(stock_file,parse_dates=['Datetime'], index_col=['Datetime'])
    except ValueError: # bc yfinance day = Date, intraday datetime
        df = pd.read_csv(stock_file,parse_dates=['Date'], index_col=['Date'])
    # todo cut out weekend (non trading day)
    df = df[df.index.dayofweek < 5]
    #df = df[df.columns[1:]] # drop date
    filename = 'scalers/%s.scaler.gz'%stock_file.split("data/")[1].lower()

    def datafix(data):
        return data[["Open","High","Low","Close","Volume"]]
    if len(df.columns) == 6:
        df = datafix(df)
    elif len(df.columns) != 5:
        raise Exception("Something is not right with data, should be 4 columns",df.columns)
    print(df.columns)
    if "train" in stock_file:
        scaler = MinMaxScaler((0,100)) # bigger values = stronger training
        dfscaled = scaler.fit_transform(df)
        dfscaled = pd.DataFrame(dfscaled,columns=df.columns)
        # write scaler to file for later
        joblib.dump(scaler,filename)
    elif "test" in stock_file:
        newname = filename.replace("test","train")
        scaler = joblib.load(newname)
        dfscaled = scaler.transform(df)
        dfscaled = pd.DataFrame(dfscaled,columns=df.columns)
    elif "all" in stock_file:
        newname = filename.replace("all","train")
        scaler = joblib.load(newname)
        dfscaled = scaler.transform(df)
        dfscaled = pd.DataFrame(dfscaled,columns=df.columns)

    # add ta features
    # dfscaled = add_all_ta_features(dfscaled,open="Open", high="High", low="Low", close="Close", volume="Volume")
    # to numpy and reduce
    dfscaled = dfscaled["Close"]
    dfscaled = dfscaled.values
    
    return dfscaled

def switch_k_backend_device():
    """ Switches `keras` backend from GPU to CPU if required.

    Faster computation on CPU (if using tensorflow-gpu).
    """
    #is really faster.
    print("switching to TensorFlow for CPU")
    os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
import numpy as np


def sigmoid(x):
    """Performs sigmoid operation
    """
    try:
        if x < 0:
            return 1 - 1 / (1 + np.exp(x))
        else:
            return 1 / (1 + np.exp(-x))
    except Exception as err:
        print("Error in sigmoid: " + err)

# def sigmoid(x):
#     return 1/(1 + np.exp(-x)) 

def get_state(data, t, n_days):
    """Returns an n-day state representation ending at time t
    """
    #blocks = []
    #for feature in datan.columns:
    #feature = "Close"
    #data = list(datan[feature])
    if len(data) == 0:
        raise Exception("DATA IS ZERO!!! CHECK YFINANCE OUTPUT")
    d = t - n_days - 1
    block = []
    if d >= 0:
        block = data[d: t + 1] 
    else: 
        block = data[0:d] # pad with t0
    res = []
    for i in range(n_days - 1):
        x = sigmoid(block[i + 1] - block[i]) # x is number
        res.append(x)
    return np.array([res])

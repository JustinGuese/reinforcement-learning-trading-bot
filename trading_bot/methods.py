import numpy as np

from tqdm import tqdm

from .utils import (
    format_currency,
    format_position
)
from .ops import (
    get_state
)

SAVEEVERY = 50  # save every x episodes


def train_model(agent, episode, data, ep_count=100, batch_size=32, window_size=10):
    total_profit = 0
    data_length = len(data) - 1

    agent.inventory = []
    avg_loss = []

    state = get_state(data, 0, window_size + 1)

    isShort = False
    hasPosition = False

    for t in tqdm(range(data_length), total=data_length, leave=True, desc='Episode {}/{}'.format(episode, ep_count)):        
        reward = 0
        COMMISSIONPCT = 0.00125 # the higher the more penalty for small trades
        IDLEPUNISH = 0.00001
        next_state = get_state(data, t + 1, window_size + 1)

        # select an action
        action = agent.act(state)

       
        if not hasPosition:
            # BUY long position
            if action == 1:
                agent.inventory.append(data[t])
                isShort = False
                hasPosition = True
                reward = IDLEPUNISH # small reward bc action done
            # Buy short position
            elif action == 2:
                agent.inventory.append(data[t])
                isShort = True
                hasPosition = True
                reward = IDLEPUNISH # small reward bc action done
            # HOLD
            else:
                pass
        else: # if there is an open position
            # BUY - if it is a short close
            if action == 1 and isShort:
                bought_price = agent.inventory.pop(0)
                delta = -(data[t] - bought_price) 
                reward = delta - (COMMISSIONPCT * data[t])
                total_profit += reward
                hasPosition = False
            # buy sig and only long
            elif action == 1 and not isShort: 
                # dont buy new stocks, but punish action bc should only choose sell then
                reward = -IDLEPUNISH
            # Sell signal if we have a long position
            elif action == 2 and not isShort:
                bought_price = agent.inventory.pop(0)
                delta = data[t] - bought_price
                reward = delta - (COMMISSIONPCT * data[t])
                total_profit += reward
                hasPosition = False
            # sell signal and have short
            elif action == 2 and isShort:
                # dont buy new stocks, but punish action bc should only choose sell then
                reward = -IDLEPUNISH
            # HOLD
            else:
                pass

        done = (t == data_length - 1)
        agent.remember(state, action, reward, next_state, done)

        if len(agent.memory) > batch_size:
            loss = agent.train_experience_replay(batch_size)
            avg_loss.append(loss)

        state = next_state

    if episode % SAVEEVERY == 0:
        agent.save(episode)

    return (episode, ep_count, total_profit, np.mean(np.array(avg_loss)))



def evaluate_model(agent, data, window_size, debug):
    total_profit = 0
    data_length = len(data) - 1

    history = []
    agent.inventory = []
    
    state = get_state(data, 0, window_size + 1)
    actionCollection = []
    hasPosition = False
    isShort = False
    COMMISSIONPCT = 0.00125
    for t in range(data_length):        
        reward = 0
        next_state = get_state(data, t + 1, window_size + 1)
        
        # select an action
        action = agent.act(state, is_eval=True)
        # BUY
        if not hasPosition:
            # BUY long position
            if action == 1:
                agent.inventory.append(data[t])
                isShort = False
                hasPosition = True
                reward = 0 # small reward bc action done
            # Buy short position
            elif action == 2:
                agent.inventory.append(data[t])
                isShort = True
                hasPosition = True
                reward = 0 # small reward bc action done
            # HOLD
            else:
                pass
        else: # if there is an open position
            # BUY - if it is a short close
            if action == 1 and isShort:
                bought_price = agent.inventory.pop(0)
                delta = -(data[t] - bought_price) 
                reward = delta - (COMMISSIONPCT * data[t])
                total_profit += reward
                hasPosition = False
            # buy sig and only long
            elif action == 1 and not isShort: 
                # dont buy new stocks, but punish action bc should only choose sell then
                reward = 0
            # Sell signal if we have a long position
            elif action == 2 and not isShort:
                bought_price = agent.inventory.pop(0)
                delta = data[t] - bought_price
                reward = delta - (COMMISSIONPCT * data[t])
                total_profit += reward
                hasPosition = False
            # sell signal and have short
            elif action == 2 and isShort:
                # dont buy new stocks, but punish action bc should only choose sell then
                reward = 0
            # HOLD
            else:
                pass

        done = (t == data_length - 1)
        agent.memory.append((state, action, reward, next_state, done))

        state = next_state
        actionCollection.append(action)
        if done:
            #print("Final decision: ",dec, " at ",format_currency(data[t]))
            return total_profit, history, actionCollection

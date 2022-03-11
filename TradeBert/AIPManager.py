from  tradingsystem import TradingSystem
from  tradingsystem import AlpacaPaperSocket
import time
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from keras.models import Sequential
from keras.layers import Dense

class PortfolioManagementSystem(TradingSystem):

    def __init__(self):
        super().__init__(AlpacaPaperSocket(), 'IBM', 604800, 1, 'AI_PM')


    def place_buy_order(self, symb):
        self.api.submit_order(
                symbol=symb,
                qty=1,
                side='buy',
                type='market',
                time_in_force='day',
            )

    def place_sell_order(self, symb):
        self.api.submit_order(
            symbol=symb,
            qty=1,
            side='sell',
            type='market',
            time_in_force='day',
        )
    def system_loop(self):
        positions = self.api.get_positions()
        # active_positions_to_check = {}  # key is stock ticker, value is stock purchase price
        # all_active_positions = {}  # key is stock ticker, value is stock purchase price
        # for position in positions:  # todo also add orders
        #     active_positions_to_check[position.symbol] = float(position.cost_basis)  # cost basis not working well
        
        # Variables for weekly close
        this_weeks_close = 0
        last_weeks_close = 0
        delta = 0
        day_count = 0
        while(True):
            # Wait a day to request more data
            time.sleep(1440)
            # Request EoD data for IBM
            for position in positions:
                data_req = self.api.get_barset(position.symbol, timeframe='1D', limit=1).df
                # Construct dataframe to predict
                x = pd.DataFrame(
                    data=[[
                        data_req['IBM']['close'][0]]], columns='Close'.split()
                )
                if(day_count == 7):
                    day_count = 0
                    last_weeks_close = this_weeks_close
                    this_weeks_close = x['Close']
                    delta = this_weeks_close - last_weeks_close

                    # AI choosing to buy, sell, or hold
                    if np.around(self.AI.network.predict([delta])) <= -.5:
                        self.place_sell_order()

                    elif np.around(self.AI.network.predict([delta]) >= .5):
                        self.place_buy_order()
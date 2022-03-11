import alpaca_trade_api as tradeapi
import threading
from datetime import datetime
import constants as const
import logging
import numpy as np
import time


SEC_KEY = 'cWUIGDGGhGsqjSauMhgcviFr6dlGkQbTtNwXIoJO'  # Enter Your Secret Key Here
PUB_KEY = 'PKW31LNZNE7P9QCCI6MF'  # Enter Your Public Key Here
# This is the base URL for paper trading
BASE_URL = 'https://paper-api.alpaca.markets'
# For real trading, don't enter a base_url
api = tradeapi.REST(key_id=PUB_KEY, secret_key=SEC_KEY, base_url=BASE_URL)
Log_Format = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename = "logs/logfile.log", filemode = "w", format = Log_Format,level = logging.DEBUG)
logger = logging.getLogger()

class alpacaapi():

    def __init__(self):
        self.api = api = tradeapi.REST(
            key_id=PUB_KEY, secret_key=SEC_KEY, base_url=BASE_URL)
        self.account = self.api.get_account()
        self.api.list_positions()
        logger.debug("Account Status: ", self.account.status)

    def sell_position(self, ticker_symbol: str):
        self.api.close_position(ticker_symbol)
        logger.debug("Closed", ticker_symbol, "position")

    def sell_all_positions(self):
        self.api.close_all_positions()
        self.api.cancel_all_orders()
        logger.debug("Closed all positions")

    def get_positions_tickers(self):
        positions = self.api.list_positions()
        positions_tickers = []
        for position in positions:  # add order ?
            positions_tickers.append(position.symbol)
        return positions_tickers

    def get_positions(self):
        positions = self.api.list_positions()
        return positions

    def create_order(self, ticker_symbol: str, quantity: int):
        self.api.submit_order(symbol=ticker_symbol, qty=quantity,
                              side='buy', type='market', time_in_force='day')
        logger.debug(quantity, ticker_symbol, "ordered")

class stocktrader():
    def daytrading_stock_analyzer(stocks):
      for stock_ticker in stocks: #purchases stocks based on daytrading patterns
          try:
              stock_score = 0
              stock_score += sa.moving_average_checker(stock_ticker)
              stock_score += sa.volume_checker(stock_ticker)
              if stock_score >= 0.2 and stock_ticker not in all_active_positions.keys():
                  alpaca.create_order(stock_ticker, 1) #todo: calculate order amount
                  active_positions_to_check[stock_ticker] = sdg.get_current_stock_data(stock_ticker)['Close']
                  all_active_positions[stock_ticker] = sdg.get_current_stock_data(stock_ticker)['Close']
                  print("Based on daytrading pattern analysis, buying", stock_ticker, "Stock Score: ", stock_score)
          except Exception as e:
              pass
    
    def stock_position_analyzer():
        while True:
            for position in active_positions_to_check.keys():
                threading.Thread(target=check_perform_sell, args=(position, active_positions_to_check[position])).start()
            active_positions_to_check.clear()

    def check_perform_sell(stock_ticker, purchase_price):
        while True:
            current_stock_price = sdg.get_current_stock_data(stock_ticker)['Close']
            price_change_percent = util.calculate_price_change(current_stock_price, all_active_positions[stock_ticker])
            print("Checking", stock_ticker, "Gains/Losses", price_change_percent, "Price: $", current_stock_price) 
            if sa.moving_average_checker(stock_ticker) < 0 or price_change_percent <= -const.MAX_STOP_LOSS_PERCENT or sa.volume_checker(stock_ticker) < 0:
                alpaca.sell_position(stock_ticker)
                del all_active_positions[stock_ticker]
                break

if __name__ == "__main__":
    alpapi = alpacaapi()
    trader = stocktrader()
    positions = alpapi.get_positions()
    active_positions_to_check = {}  # key is stock ticker, value is stock purchase price
    all_active_positions = {}  # key is stock ticker, value is stock purchase price
    for position in positions:  # todo also add orders
        active_positions_to_check[position.symbol] = float(
            position.cost_basis)  # cost basis not working well

    while True:
            try:
                logger.debug("Initial iteration Stock Scanning")
                current_time = datetime.now().strftime("%H:%M")
                # current_time = "12:01"
                if current_time > const.STOCK_MARKET_OPEN_TIME and current_time < const.STOCK_MARKET_CLOSE_TIME:
                    if first_time_run:
                        threading.Thread(target=trader.stock_position_analyzer).start()
                        first_time_run = False
                    active_stocks = scraper.active_stocks()
                    partitioned_stocks = util.partition_array(active_stocks, const.STOCK_SCANNER_PARTITION_COUNT)
                    for partition in partitioned_stocks:
                        threading.Thread(target=daytrading_stock_analyzer, args=[partition]).start()
                else:
                    alpapi.sell_all_positions()
                    logger.debug("Market Close")
                    for stock_ticker in const.STOCKS_TO_CHECK: #purchases stocks based on news info
                        threading.Thread(target=news_stock_analyzer, args=(stock_ticker,)).start()
                    time.sleep(360000)
            except Exception as e:
                logger.debug("Restarting")
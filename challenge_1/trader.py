# The Python code below is the minimum code that is required in a submission file:
# 1. The "datamodel" imports at the top. Using the typing library is optional.
# 2. A class called "Trader", this class name should not be changed.
# 3. A run function that takes a tradingstate as input and outputs a "result" dict.

from typing import Dict, List
from datamodel import OrderDepth, TradingState, Order
import numpy as np

POS_LIMIT_PEARLS = 20
BUY_PRICE_PEARLS = 9998
SELL_PRICE_PEARLS = 10002
POS_LIMIT_BANANAS = 20

class Trader:

    
    def __init__(self):
        self.ma = 0
        self.ma_count = 0
        self.ma_list = np.empty(20)
        self.profit_pearls = 0
        self.profit_bananas = 0
        
    
    def run(self, state: TradingState) -> Dict[str, List[Order]]:
        """
	    Takes all buy and sell orders for all symbols as an input,
	    and outputs a list of orders to be sent
	    """
        result = {}

        for product in state.order_depths.keys():
            if product == 'PEARLS':
                orders: list[Order] = []
                buy_volume = POS_LIMIT_PEARLS - state.position.get(product, 0)
                sell_volume = POS_LIMIT_PEARLS + state.position.get(product, 0)
                orders.append(Order(product, BUY_PRICE_PEARLS, buy_volume))
                orders.append(Order(product, SELL_PRICE_PEARLS, -sell_volume))

                
                result[product] = orders
            if product == 'BANANAS':
                orders: list[Order] = []
                order_depth: OrderDepth = state.order_depths[product]
                best_ask = min(order_depth.sell_orders.keys())
                best_bid = max(order_depth.buy_orders.keys())
                midprice = (best_ask+best_bid)/2
                rolling_mean = 0
                if self.ma_count == 19:
                    self.ma_list = np.insert(self.ma_list, self.ma_count, midprice)
                    rolling_mean = np.mean(self.ma_list)
                    self.ma_list = np.delete(self.ma_list, 0)

                else:
                    self.ma_list = np.delete(self.ma_list, self.ma_count)
                    self.ma_list = np.insert(self.ma_list, self.ma_count, midprice)
                    self.ma_count += 1
                    if self.ma_count == 19:
                        self.ma_list = np.delete(self.ma_list, self.ma_count)
                if rolling_mean != 0:
                    if best_ask + 2 <= rolling_mean:
                        buy_volume = POS_LIMIT_BANANAS - state.position.get(product, 0)
                        orders.append(Order(product, best_ask, buy_volume))
                    elif best_bid >= rolling_mean + 1 and state.position.get(product, 0) > 0:
                        sell_volume = state.position.get(product, 0)
                        orders.append(Order(product, best_bid, -sell_volume))
                    elif best_bid - 2 >= rolling_mean:
                        sell_volume = POS_LIMIT_BANANAS + state.position.get(product, 0)
                        orders.append(Order(product, best_bid, -sell_volume))
                    elif best_ask <= rolling_mean - 1 and state.position.get(product, 0) < 0:
                        buy_volume = state.position.get(product, 0)
                        orders.append(Order(product, best_ask, -buy_volume))
                    result[product] = orders

        return result
# The Python code below is the minimum code that is required in a submission file:
# 1. The "datamodel" imports at the top. Using the typing library is optional.
# 2. A class called "Trader", this class name should not be changed.
# 3. A run function that takes a tradingstate as input and outputs a "result" dict.

from typing import Dict, List
from datamodel import OrderDepth, TradingState, Order
import numpy as np

import json
from datamodel import Order, ProsperityEncoder, Symbol, TradingState
from typing import Any

POS_LIMIT_PEARLS = 20
BUY_PRICE_PEARLS = 9998
SELL_PRICE_PEARLS = 10002
POS_LIMIT_BANANAS = 20
POS_LIMIT_COCONUTS = 600
POS_LIMIT_PINA_COLADAS = 300

class Logger:
    def __init__(self) -> None:
        self.logs = ""

    def print(self, *objects: Any, sep: str = " ", end: str = "\n") -> None:
        self.logs += sep.join(map(str, objects)) + end

    def flush(self, state: TradingState, orders: dict[Symbol, list[Order]]) -> None:
        print(json.dumps({
            "state": state,
            "orders": orders,
            "logs": self.logs,
        }, cls=ProsperityEncoder, separators=(",", ":"), sort_keys=True))

        self.logs = ""

logger = Logger()


class Trader:

    
    def __init__(self):
        self.ma = 0
        self.ma_count = 0
        self.ma_list = np.empty(20)
        self.pina_coladas_update = False
        self.pina_coladas_bid_price = self.pina_coladas_ask_price = self.pina_coladas_bid_volume = self.pina_coladas_ask_volume = 0
        self.coconuts_update = False
        self.coconuts_bid_price = self.coconuts_ask_price = self.coconuts_bid_volume = self.coconuts_ask_volume = 0
        
    
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

            if product == 'COCONUTS':
                orders_coconuts: list[Order] = []
                orders_pina_coladas: list[Order] = []
                order_depth: OrderDepth = state.order_depths[product]
                self.coconuts_bid_price = max(order_depth.buy_orders.keys())
                self.coconuts_bid_volume = order_depth.buy_orders.get(self.coconuts_bid_price)
                self.coconuts_ask_price = min(order_depth.sell_orders.keys())
                self.coconuts_ask_volume = order_depth.sell_orders.get(self.coconuts_ask_price)
                self.coconuts_update = True
                
                if self.pina_coladas_update == True:
                    print('here 1')
                    # here compute if we want to send an order and then also send the orders
                    # logic:
                    # if pos is neutral then we want to enter when products diverge
                    # if pos not neutral enter more when diverge even more or exit when we converge back together
                    # first case entering positions
                    if self.coconuts_ask_price <= self.pina_coladas_bid_price - 7028:
                        # ente into the position
                        buy_volume = int(min([POS_LIMIT_COCONUTS-state.position.get(product, 0), (abs(POS_LIMIT_PINA_COLADAS+state.position.get('PINA_COLADAS', 0)))*1.875, abs(self.coconuts_ask_volume), self.pina_coladas_bid_volume*1.875]))
                        sell_volume = int(-buy_volume/1.875)
                        orders_coconuts.append(Order(product, self.coconuts_ask_price, buy_volume))
                        orders_pina_coladas.append(Order('PINA_COLADAS', self.pina_coladas_bid_price, sell_volume))
                    elif self.coconuts_bid_price >= self.pina_coladas_ask_price - 6988:
                        buy_volume = int(min([(POS_LIMIT_COCONUTS+state.position.get(product, 0))/1.875, (POS_LIMIT_PINA_COLADAS-state.position.get('PINA_COLADAS', 0)), self.coconuts_bid_volume/1.875, abs(self.pina_coladas_ask_volume)]))
                        sell_volume = int(-buy_volume*1.875)
                        orders_pina_coladas.append(Order('PINA_COLADAS', self.pina_coladas_ask_price, buy_volume))
                        orders_coconuts.append(Order(product, self.coconuts_bid_price, sell_volume))
                    if state.position.get(product, 0) > 0:
                        if self.coconuts_bid_price >= self.pina_coladas_ask_price - 7008:
                            # exit the position
                            buy_volume = int(min([abs(state.position.get(product, 0))/1.875,self.coconuts_bid_volume/1.875, abs(self.pina_coladas_ask_volume)]))
                            sell_volume = -int(buy_volume*1.875)
                            orders_coconuts.append(Order(product, self.coconuts_bid_price, sell_volume))
                            orders_pina_coladas.append(Order('PINA_COLADAS', self.pina_coladas_ask_price, buy_volume))
                    elif state.position.get(product, 0) < 0:
                        if self.coconuts_ask_price <= self.pina_coladas_bid_price - 7008:
                            buy_volume = int(min([(abs(state.position.get(product, 0))), abs(self.coconuts_ask_volume), (self.pina_coladas_bid_volume)*1.875]))
                            sell_volume = int(-buy_volume/1.875)
                            orders_pina_coladas.append(Order('PINA_COLADAS', self.pina_coladas_bid_price, sell_volume))
                            orders_coconuts.append(Order(product, self.coconuts_ask_price, buy_volume))
                        
                    self.coconuts_update = False
                    self.pina_coladas_update = False
                result[product] = orders_coconuts
                result['PINA_COLADAS'] = orders_pina_coladas

            if product == 'PINA_COLADAS':
                orders_coconuts: list[Order] = []
                orders_pina_coladas: list[Order] = []
                order_depth: OrderDepth = state.order_depths[product]
                self.pina_coladas_bid_price = max(order_depth.buy_orders.keys())
                self.pina_coladas_bid_volume = order_depth.buy_orders.get(self.pina_coladas_bid_price)
                self.pina_coladas_ask_price = min(order_depth.sell_orders.keys())
                self.pina_coladas_ask_volume = order_depth.sell_orders.get(self.pina_coladas_ask_price)
                self.pina_coladas_update = True
                if state.position.get('COCONUTS', 0) == 0 and state.position.get('PINA_COLADAS', 0) != 0:
                    if state.position.get('PINA_COLADAS', 0) > 0:
                        orders_pina_coladas.append(Order('PINA_COLADAS', self.pina_coladas_bid_price, -state.position.get('PINA_COLADAS', 0)))
                    else:
                        orders_pina_coladas.append(Order('PINA_COLADAS', self.pina_coladas_ask_price, -state.position.get('PINA_COLADAS', 0)))
                if state.position.get('COCONUTS', 0) != 0 and state.position.get('PINA_COLADAS', 0) == 0:
                    if state.position.get('COCONUTS', 0) > 0:
                        orders_coconuts.append(Order('COCONUTS', self.coconuts_bid_price, -state.position.get('COCONUTS', 0)))
                    else:
                        orders_coconuts.append(Order('COCONUTS', self.coconuts_ask_price, -state.position.get('COCONUTS', 0)))
                
                if self.coconuts_update == True:

                    # here compute if we want to send an order and then also send the orders
                    # logic:
                    # if pos is neutral then we want to enter when products diverge
                    # if pos not neutral enter more when diverge even more or exit when we converge back together
                    # first case entering positions
                    if self.coconuts_ask_price <= self.pina_coladas_bid_price - 7048:
                        # ente into the position
                        
                        buy_volume = int(min([POS_LIMIT_COCONUTS-state.position.get('COCONUTS', 0), (abs(POS_LIMIT_PINA_COLADAS+state.position.get(product, 0)))*1.875, abs(self.coconuts_ask_volume), self.pina_coladas_bid_volume*1.875]))
                        sell_volume = int(-buy_volume/1.875)
                        orders_coconuts.append(Order('COCONUTS', self.coconuts_ask_price, buy_volume))
                        orders_pina_coladas.append(Order(product, self.pina_coladas_bid_price, sell_volume))
                    elif self.coconuts_bid_price >= self.pina_coladas_ask_price - 6968:
                        buy_volume = int(min([(POS_LIMIT_COCONUTS+state.position.get('COCONUTS', 0))/1.875, (POS_LIMIT_PINA_COLADAS-state.position.get(product, 0)), self.coconuts_bid_volume/1.875, abs(self.pina_coladas_ask_volume)]))
                        sell_volume = int(-buy_volume*1.875)
                        orders_pina_coladas.append(Order(product, self.pina_coladas_ask_price, buy_volume))
                        orders_coconuts.append(Order('COCONUTS', self.coconuts_bid_price, sell_volume))
                    if state.position.get('COCONUTS', 0) > 0:
                        if self.coconuts_bid_price >= self.pina_coladas_ask_price - 7033:
                            # exit the position
                            buy_volume = int(min([abs(state.position.get('COCONUTS', 0))/1.875,self.coconuts_bid_volume/1.875, abs(self.pina_coladas_ask_volume)]))
                            sell_volume = -int(buy_volume*1.875)
                            orders_coconuts.append(Order('COCONUTS', self.coconuts_bid_price, sell_volume))
                            orders_pina_coladas.append(Order(product, self.pina_coladas_ask_price, buy_volume))
                    elif state.position.get('COCONUTS', 0) < 0:
                        # print('here test exit 1')
                        # print('spread: ', self.pina_coladas_bid_price - self.coconuts_ask_price)
                        if self.coconuts_ask_price <= self.pina_coladas_bid_price - 6982:
                            # print('here test exit 2')
                            buy_volume = int(min([(abs(state.position.get('COCONUTS', 0))), abs(self.coconuts_ask_volume), (self.pina_coladas_bid_volume)*1.875]))
                            sell_volume = int(-buy_volume/1.875)
                            # print('sell volume: ', sell_volume)
                            # print('buy volume: ', buy_volume)
                            orders_pina_coladas.append(Order(product, self.pina_coladas_bid_price, sell_volume))
                            orders_coconuts.append(Order('COCONUTS', self.coconuts_ask_price, buy_volume))
                    self.coconuts_update = False
                    self.pina_coladas_update = False
                result[product] = orders_pina_coladas
                result['COCONUTS'] = orders_coconuts

        logger.flush(state, orders)
        return result
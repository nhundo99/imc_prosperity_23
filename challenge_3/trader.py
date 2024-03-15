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
import pandas as pd


POS_LIMIT_PEARLS = 20
BUY_PRICE_PEARLS = 9998
SELL_PRICE_PEARLS = 10002
POS_LIMIT_BANANAS = 20
POS_LIMIT_COCONUTS = 600
POS_LIMIT_PINA_COLADAS = 300
POS_LIMIT_BERRIES = 250
POS_LIMIT_DIVING_GEAR = 50

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
        self.coconuts_mid_price = self.pina_coladas_mid_price = 0
        self.df_dolphin_sightings = pd.DataFrame({'change': [], 'rolling_change': []})
        self.rolling_sightings = 0
        self.gear_pos_inventory = False
        self.gear_neg_inventory = False
        self.gear_buy_more = False
        self.gear_sell_more = False
        self.coc_pin_spread = 0
        self.coc_pin_spread_rolling = 0
        

    
    def run(self, state: TradingState) -> Dict[str, List[Order]]:
        """
	    Takes all buy and sell orders for all symbols as an input,
	    and outputs a list of orders to be sent
	    """
        result = {}
        print('first spread: ', self.coc_pin_spread)
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
                print('here 1')
                print('coc pin spread 1: ', self.coc_pin_spread)
                orders_coconuts: list[Order] = []
                orders_pina_coladas: list[Order] = []
                order_depth: OrderDepth = state.order_depths[product]
                self.coconuts_bid_price = max(order_depth.buy_orders.keys())
                self.coconuts_bid_volume = order_depth.buy_orders.get(self.coconuts_bid_price)
                self.coconuts_ask_price = min(order_depth.sell_orders.keys())
                self.coconuts_ask_volume = order_depth.sell_orders.get(self.coconuts_ask_price)
                self.coconuts_update = True
                
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
                
                if self.pina_coladas_update == True:

                    # here compute if we want to send an order and then also send the orders
                    # logic:
                    # if pos is neutral then we want to enter when products diverge
                    # if pos not neutral enter more when diverge even more or exit when we converge back together
                    # first case entering positions
                    ratio = 1
                    denom = (state.timestamp/100)+1
                    
                    self.coconuts_mid_price = (self.coconuts_bid_price+self.coconuts_ask_price)/2
                    self.pina_coladas_mid_price = (self.pina_coladas_bid_price+self.pina_coladas_ask_price)/2
                    if self.coconuts_mid_price != 0:
                        ratio = self.pina_coladas_mid_price/self.coconuts_mid_price
                    print('current spread: ', self.coc_pin_spread)
                    if self.coconuts_mid_price != 0 and self.pina_coladas_mid_price != 0:
                        self.coc_pin_spread += self.pina_coladas_mid_price - self.coconuts_mid_price
                        self.coc_pin_spread_rolling = self.coc_pin_spread/denom
                    print('coc midprice: ', self.coconuts_mid_price)
                    print('pin midprice: ', self.pina_coladas_mid_price)                    
                    print('current spread: ', self.coc_pin_spread)
                    print('rolling spread: ', self.coc_pin_spread_rolling)
                    if denom > 40 and self.pina_coladas_bid_price - self.coconuts_ask_price >= self.coc_pin_spread_rolling + 15: # we subtract 5 from the rolling spread for the bid/ask spread and then add 20 for the trading oppurtunity
                        # ente into the position
                        buy_volume = int(min([POS_LIMIT_COCONUTS-state.position.get(product, 0), (abs(POS_LIMIT_PINA_COLADAS+state.position.get('PINA_COLADAS', 0)))*ratio, abs(self.coconuts_ask_volume), self.pina_coladas_bid_volume*ratio]))
                        sell_volume = int(-buy_volume/ratio)
                        orders_coconuts.append(Order(product, self.coconuts_ask_price, buy_volume))
                        orders_pina_coladas.append(Order('PINA_COLADAS', self.pina_coladas_bid_price, sell_volume))
                    elif denom > 40 and self.pina_coladas_ask_price - self.coconuts_bid_price <= self.coc_pin_spread_rolling - 15: # we add 5 from the rolling spread for the bid/ask spread and then subtract 20 for the trading oppurtunity
                        buy_volume = int(min([(POS_LIMIT_COCONUTS+state.position.get(product, 0))/ratio, (POS_LIMIT_PINA_COLADAS-state.position.get('PINA_COLADAS', 0)), self.coconuts_bid_volume/ratio, abs(self.pina_coladas_ask_volume)]))
                        sell_volume = int(-buy_volume*ratio)
                        orders_pina_coladas.append(Order('PINA_COLADAS', self.pina_coladas_ask_price, buy_volume))
                        orders_coconuts.append(Order(product, self.coconuts_bid_price, sell_volume))
                    if state.position.get(product, 0) > 0:
                        if self.pina_coladas_ask_price - self.coconuts_bid_price <= self.coc_pin_spread_rolling + 5:
                            # exit the position
                            buy_volume = int(min([abs(state.position.get(product, 0))/ratio,self.coconuts_bid_volume/ratio, abs(self.pina_coladas_ask_volume)]))
                            sell_volume = -int(buy_volume*ratio)
                            orders_coconuts.append(Order(product, self.coconuts_bid_price, sell_volume))
                            orders_pina_coladas.append(Order('PINA_COLADAS', self.pina_coladas_ask_price, buy_volume))
                    elif state.position.get(product, 0) < 0:
                        if self.pina_coladas_bid_price - self.coconuts_ask_price >= self.coc_pin_spread_rolling - 5:
                            buy_volume = int(min([(abs(state.position.get(product, 0))), abs(self.coconuts_ask_volume), (self.pina_coladas_bid_volume)*ratio]))
                            sell_volume = int(-buy_volume/ratio)
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
                print('here')
                print('coc pin spread: ', self.coc_pin_spread)
                
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
                    ratio = 1
                    denom = (state.timestamp/100)
                    
                    self.coconuts_mid_price = (self.coconuts_bid_price+self.coconuts_ask_price)/2
                    self.pina_coladas_mid_price = (self.pina_coladas_bid_price+self.pina_coladas_ask_price)/2
                    if self.coconuts_mid_price != 0:
                        ratio = self.pina_coladas_mid_price/self.coconuts_mid_price
                    if denom < 40:
                        self.coc_pin_spread += self.pina_coladas_mid_price - self.coconuts_mid_price
                        self.coc_pin_spread_rolling = self.coc_pin_spread/denom
                    print('current spread: ', self.coc_pin_spread)
                    print('rolling spread: ', self.coc_pin_spread_rolling)
                    if denom > 40 and self.pina_coladas_bid_price - self.coconuts_ask_price >= self.coc_pin_spread_rolling + 5: # we subtract 5 from the rolling spread for the bid/ask spread and then add 10 for the trading oppurtunity
                        # ente into the position
                        
                        buy_volume = int(min([POS_LIMIT_COCONUTS-state.position.get('COCONUTS', 0), (abs(POS_LIMIT_PINA_COLADAS+state.position.get(product, 0)))*ratio, abs(self.coconuts_ask_volume), self.pina_coladas_bid_volume*ratio]))
                        sell_volume = int(-buy_volume/ratio)
                        orders_coconuts.append(Order('COCONUTS', self.coconuts_ask_price, buy_volume))
                        orders_pina_coladas.append(Order(product, self.pina_coladas_bid_price, sell_volume))
                    elif denom > 20 and self.pina_coladas_ask_price - self.coconuts_bid_price <= self.coc_pin_spread_rolling - 5: # we add 5 from the rolling spread for the bid/ask spread and then subtract 10 for the trading oppurtunity
                        buy_volume = int(min([(POS_LIMIT_COCONUTS+state.position.get('COCONUTS', 0))/ratio, (POS_LIMIT_PINA_COLADAS-state.position.get(product, 0)), self.coconuts_bid_volume/ratio, abs(self.pina_coladas_ask_volume)]))
                        sell_volume = int(-buy_volume*ratio)
                        orders_pina_coladas.append(Order(product, self.pina_coladas_ask_price, buy_volume))
                        orders_coconuts.append(Order('COCONUTS', self.coconuts_bid_price, sell_volume))
                    if state.position.get('COCONUTS', 0) > 0:
                        if self.pina_coladas_ask_price - self.coconuts_bid_price <= self.coc_pin_spread_rolling + 5:
                            # exit the position
                            buy_volume = int(min([abs(state.position.get('COCONUTS', 0))/ratio,self.coconuts_bid_volume/ratio, abs(self.pina_coladas_ask_volume)]))
                            sell_volume = -int(buy_volume*ratio)
                            orders_coconuts.append(Order('COCONUTS', self.coconuts_bid_price, sell_volume))
                            orders_pina_coladas.append(Order(product, self.pina_coladas_ask_price, buy_volume))
                    elif state.position.get('COCONUTS', 0) < 0:
                        # print('here test exit 1')
                        # print('spread: ', self.pina_coladas_bid_price - self.coconuts_ask_price)
                        if self.pina_coladas_bid_price - self.coconuts_ask_price >= self.coc_pin_spread_rolling - 5:
                            # print('here test exit 2')
                            buy_volume = int(min([(abs(state.position.get('COCONUTS', 0))), abs(self.coconuts_ask_volume), (self.pina_coladas_bid_volume)*ratio]))
                            sell_volume = int(-buy_volume/ratio)
                            # print('sell volume: ', sell_volume)
                            # print('buy volume: ', buy_volume)
                            orders_pina_coladas.append(Order(product, self.pina_coladas_bid_price, sell_volume))
                            orders_coconuts.append(Order('COCONUTS', self.coconuts_ask_price, buy_volume))
                    self.coconuts_update = False
                    self.pina_coladas_update = False
                result[product] = orders_pina_coladas
                result['COCONUTS'] = orders_coconuts
            
            if product == 'BERRIES':
                orders: list[Order] = []
                order_depth: OrderDepth = state.order_depths[product]
                best_ask = min(order_depth.sell_orders.keys())
                best_bid = max(order_depth.buy_orders.keys())
                midprice = (best_bid+best_ask)/2
                if state.timestamp > 100000 and state.timestamp < 300000 and state.position.get(product, 0) < POS_LIMIT_BERRIES:
                    # buy low at beginning of day
                    buy_volume = 1
                    orders.append(Order(product, best_ask, buy_volume))
                if state.timestamp > 460000 and state.timestamp < 550000 and -state.position.get(product, 0) < POS_LIMIT_BERRIES:
                    # sell high at the middle of the day and enter short position
                    sell_volume = -1
                    orders.append(Order(product, best_bid, sell_volume))
                if state.timestamp > 700000 and state.timestamp < 800000 and state.position.get(product, 0) < 0:
                    # # buy back the stock to get back to a neutral position
                    buy_volume = 1
                    orders.append(Order(product, best_ask, buy_volume))
                result[product] = orders
            
            if product == 'DOLPHIN_SIGHTINGS':
                # here we want to just calculate the rolling sum of the change in the price
                new_sightings = state.observations.get(product, 0)
                index = len(self.df_dolphin_sightings.index)
                self.df_dolphin_sightings.loc[index, 'change'] = new_sightings
                # next part can also be done in one line but maye we want the older information to optimize
                self.df_dolphin_sightings.loc[index, 'rolling_change'] = self.df_dolphin_sightings['change'].rolling(5).sum().loc[index]
                self.rolling_sightings = self.df_dolphin_sightings.loc[index, 'rolling_change']
            
            if product == 'DIVING_GEAR':
                orders: list[Order] = []
                order_depth: OrderDepth = state.order_depths[product]
                bid_price = max(order_depth.buy_orders.keys())
                ask_price = min(order_depth.sell_orders.keys())
                bid_volume = order_depth.buy_orders.get(bid_price)
                ask_volume = order_depth.sell_orders.get(ask_price)
                curr_pos = state.position.get(product, 0)
                print('rolling sightsings: ', self.rolling_sightings)
                if self.rolling_sightings > 6 or self.gear_buy_more:
                    # buy as much diving gear as possible
                    # maybe also make a variable that we then have a diving gear inventory,
                    # so that we know that we have to sell it again at one point
                    buy_volume = min(POS_LIMIT_DIVING_GEAR - curr_pos, abs(ask_volume))
                    orders.append(Order(product, ask_price, buy_volume))
                    if curr_pos + buy_volume > 0:
                        self.gear_pos_inventory = True
                    if curr_pos + buy_volume < POS_LIMIT_DIVING_GEAR:
                        self.gear_buy_more = True
                    else:
                        self.gear_buy_more = False
                if self.rolling_sightings > 2 and self.gear_neg_inventory:
                    # buy back the remaining inventory
                    buy_volume = min(abs(curr_pos), abs(ask_volume))
                    orders.append(Order(product, ask_price, buy_volume))
                    if curr_pos + buy_volume == 0:
                        self.gear_neg_inventory = False
                    else:
                        self.gear_neg_inventory = True
                if self.rolling_sightings < -6 or self.gear_sell_more:
                    # sell as much diving gear as possible
                    # maybe also make a variable that we then have a negative diving gear inventory,
                    # so that we know that we have to sell it again at one point
                    sell_volume = -min(POS_LIMIT_DIVING_GEAR + state.position.get(product, 0), abs(bid_volume))
                    orders.append(Order(product, bid_price, sell_volume))
                    if curr_pos + sell_volume < 0:
                        self.gear_neg_inventory = True
                    if curr_pos + sell_volume > -POS_LIMIT_DIVING_GEAR:
                        self.gear_sell_more = True
                    else:
                        self.gear_sell_more = False
                if self.rolling_sightings < -2 and self.gear_pos_inventory:
                    # sell the remaining inventory
                    sell_volume = -min(curr_pos, bid_volume)
                    orders.append(Order(product, bid_price, sell_volume))
                    if curr_pos + sell_volume == 0:
                        self.gear_pos_inventory = False
                    else:
                        self.gear_pos_inventory = True



        logger.flush(state, orders)
        return result
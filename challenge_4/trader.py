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
POS_LIMIT_BAGUETTE = 150
POS_LIMIT_DIP = 300
POS_LIMIT_UKULELE = 70
POS_LIMIT_PICNIC_BASKET = 70

class Logger:
    # Set this to true, if u want to create
    # local logs
    local: bool 
    # this is used as a buffer for logs
    # instead of stdout
    local_logs: dict[int, str] = {}

    def __init__(self, local=False) -> None:
        self.logs = ""
        self.local = local

    def print(self, *objects: Any, sep: str = " ", end: str = "\n") -> None:
        self.logs += sep.join(map(str, objects)) + end

    def flush(self, state: TradingState, orders: dict[Symbol, list[Order]]) -> None:
        output = json.dumps({
            "state": state,
            "orders": orders,
            "logs": self.logs,
        }, cls=ProsperityEncoder, separators=(",", ":"), sort_keys=True)
        if self.local:
            self.local_logs[state.timestamp] = output
        print(output)

        self.logs = ""


class Trader:

    logger = Logger(local=True)

    def __init__(self):
        self.dolphins_sightings_yesterday = 0
        
    
    

    
    def run(self, state: TradingState) -> Dict[str, List[Order]]:
        """
	    Takes all buy and sell orders for all symbols as an input,
	    and outputs a list of orders to be sent
	    """
        result = {}
        picnic_bucket_update = False
        dip_update = False
        baguette_update = False
        ukulele_update = False
        picnic_bucket_midprice = dip_midprice = baguette_midprice = ukulele_midprice = 0
        picnic_bucket_ask_price = picnic_bucket_bid_price = picnic_bucket_ask_volume = picnic_bucket_bid_volume = 0
        dip_ask_price = dip_bid_price = dip_ask_volume = dip_bid_volume = 0
        baguette_ask_price = baguette_bid_price = baguette_ask_volume = baguette_bid_volume = 0
        ukulele_ask_price = ukulele_bid_price = ukulele_ask_volume = ukulele_bid_volume = 0
        
        for product in state.order_depths.keys():
            
            

            
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
            
            if product == 'PEARLS':
                orders: list[Order] = []
                buy_volume = POS_LIMIT_PEARLS - state.position.get(product, 0)
                sell_volume = POS_LIMIT_PEARLS + state.position.get(product, 0)
                orders.append(Order(product, BUY_PRICE_PEARLS, buy_volume))
                orders.append(Order(product, SELL_PRICE_PEARLS, -sell_volume))

                
                result[product] = orders
            
            if product == 'PICNIC_BASKET' or product == 'DIP' or product == 'BAGUETTE' or product == 'UKULELE':
                
                if product == 'PICNIC_BASKET':
                    order_depth: OrderDepth = state.order_depths[product]
                    picnic_bucket_bid_price = max(order_depth.buy_orders.keys())
                    picnic_bucket_ask_price = min(order_depth.sell_orders.keys())
                    picnic_bucket_bid_volume = order_depth.buy_orders.get(picnic_bucket_bid_price, 0)
                    picnic_bucket_ask_volume = order_depth.sell_orders.get(picnic_bucket_ask_price, 0)
                    picnic_bucket_midprice = (picnic_bucket_bid_price+picnic_bucket_ask_price)/2
                    picnic_bucket_update = True
                if product == 'DIP':
                    order_depth: OrderDepth = state.order_depths[product]
                    dip_bid_price = max(order_depth.buy_orders.keys())
                    dip_ask_price = min(order_depth.sell_orders.keys())
                    dip_bid_volume = order_depth.buy_orders.get(dip_bid_price, 0)
                    dip_ask_volume = order_depth.sell_orders.get(dip_ask_price, 0)
                    dip_midprice = (dip_bid_price+dip_ask_price)/2
                    dip_update = True
                if product == 'BAGUETTE':
                    order_depth: OrderDepth = state.order_depths[product]
                    baguette_bid_price = max(order_depth.buy_orders.keys())
                    baguette_ask_price = min(order_depth.sell_orders.keys())
                    baguette_bid_volume = order_depth.buy_orders.get(baguette_bid_price, 0)
                    baguette_ask_volume = order_depth.sell_orders.get(baguette_ask_price, 0)
                    baguette_midprice = (baguette_bid_price+baguette_ask_price)/2
                    baguette_update = True
                if product == 'UKULELE':
                    order_depth: OrderDepth = state.order_depths[product]
                    ukulele_bid_price = max(order_depth.buy_orders.keys())
                    ukulele_ask_price = min(order_depth.sell_orders.keys())
                    ukulele_bid_volume = order_depth.buy_orders.get(ukulele_bid_price, 0)
                    ukulele_ask_volume = order_depth.sell_orders.get(ukulele_ask_price, 0)
                    ukulele_midprice = (ukulele_bid_price+ukulele_ask_price)/2
                    ukulele_update = True
                if dip_update == True and baguette_update == True and ukulele_update == True and picnic_bucket_update == True:
                    orders_picnic_basket: list[Order] = []
                    orders_baguette: list[Order] = []
                    orders_dip: list[Order] = []
                    orders_ukulele: list[Order] = []
                    spread = picnic_bucket_midprice - (2*baguette_midprice + 4*dip_midprice + ukulele_midprice)
                    pos_picnic_basket = state.position.get('PICNIC_BASKET', 0)
                    pos_baguette = state.position.get('BAGUETTE', 0)
                    pos_dip = state.position.get('DIP', 0)
                    pos_ukulele = state.position.get('UKULELE', 0)
                    
                                        
                    if spread > 475: # sell bucket buy components
                        sell_volume = -min([10, abs(picnic_bucket_bid_volume),
                                            abs(ukulele_ask_volume),
                                            abs(int(baguette_ask_volume/2)),
                                            abs(int(dip_ask_volume/4)),
                                            abs(POS_LIMIT_PICNIC_BASKET+pos_picnic_basket),
                                            abs(POS_LIMIT_UKULELE-pos_ukulele),
                                            abs(int((POS_LIMIT_BAGUETTE-pos_baguette)/2)),
                                            abs(int((POS_LIMIT_DIP-pos_dip)/4))])
                        buy_volume = -sell_volume
                        orders_picnic_basket.append(Order('PICNIC_BASKET', picnic_bucket_bid_price, sell_volume))
                        orders_baguette.append(Order('BAGUETTE', baguette_ask_price, buy_volume*2))
                        orders_dip.append(Order('DIP', dip_ask_price, buy_volume*4))
                        orders_ukulele.append(Order('UKULELE', ukulele_ask_price, buy_volume))
                    
                    if spread < 275: # buy bucket sell components
                        buy_volume = min([10, abs(picnic_bucket_ask_volume),
                                          abs(ukulele_bid_volume),
                                          abs(int(baguette_bid_volume/2)),
                                          abs(int(dip_bid_volume/4)),
                                          abs(POS_LIMIT_PICNIC_BASKET-pos_picnic_basket),
                                          abs(POS_LIMIT_UKULELE+pos_ukulele),
                                          abs(int((POS_LIMIT_BAGUETTE+pos_baguette)/2)),
                                          abs(int((POS_LIMIT_DIP+pos_dip)/4))])
                        sell_volume = -buy_volume
                        orders_picnic_basket.append(Order('PICNIC_BASKET', picnic_bucket_ask_price, buy_volume))
                        orders_baguette.append(Order('BAGUETTE', baguette_bid_price, sell_volume*2))
                        orders_dip.append(Order('DIP', dip_bid_price, sell_volume*4))
                        orders_ukulele.append(Order('UKULELE', ukulele_bid_price, sell_volume))
                    if pos_picnic_basket < 0 and spread <= 375: # buy the buckets back and sell the components
                        buy_volume = min([abs(pos_picnic_basket),
                                          abs(picnic_bucket_ask_volume),
                                          abs(ukulele_bid_volume),
                                          abs(int(baguette_bid_volume/2)),
                                          abs(int(dip_bid_volume/4))])
                        sell_volume = -buy_volume
                        orders_picnic_basket.append(Order('PICNIC_BASKET', picnic_bucket_ask_price, buy_volume))
                        orders_baguette.append(Order('BAGUETTE', baguette_bid_price, sell_volume*2))
                        orders_dip.append(Order('DIP', dip_bid_price, sell_volume*4))
                        orders_ukulele.append(Order('UKULELE', ukulele_bid_price, sell_volume))
                    if pos_picnic_basket > 0 and spread >= 375: # sell the buckets and buy back the components
                        sell_volume = -min([pos_picnic_basket,
                                            abs(picnic_bucket_bid_volume),
                                            abs(ukulele_ask_volume),
                                            abs(int(baguette_ask_volume/2)),
                                            abs(int(dip_ask_volume/4))])
                        buy_volume = -sell_volume
                        orders_picnic_basket.append(Order('PICNIC_BASKET', picnic_bucket_bid_price, sell_volume))
                        orders_baguette.append(Order('BAGUETTE', baguette_ask_price, buy_volume*2))
                        orders_dip.append(Order('DIP', dip_ask_price, buy_volume*4))
                        orders_ukulele.append(Order('UKULELE', ukulele_ask_price, buy_volume))




                    dip_update = False
                    ukulele_update = False
                    baguette_update = False
                    picnic_bucket_update = False
                    result['PICNIC_BASKET'] = orders_picnic_basket
                    result['DIP'] = orders_dip
                    result['UKULELE'] = orders_ukulele
                    result['BAGUETTE'] = orders_baguette




        self.logger.flush(state, result)
        return result
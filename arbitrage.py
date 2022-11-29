import json
import copy
import winsound
from exchanges.exchanges import Exchange
from datetime import datetime

static_symbols =  ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'NEOUSDT', 'LTCUSDT', 'ADAUSDT', 'XRPUSDT', 'EOSUSDT', 'ONTUSDT', 'TRXUSDT', 'ETCUSDT', 'LINKUSDT', 'WAVESUSDT', 'ZILUSDT', 'ZECUSDT', 'DASHUSDT', 'NANOUSDT', 'THETAUSDT', 'ENJUSDT', 'MATICUSDT', 'ATOMUSDT', 'DOGEUSDT', 'DUSKUSDT','CHZUSDT', 'RVNUSDT', 'HBARUSDT', 'VITEUSDT', 'FTTUSDT', 'COTIUSDT', 'SOLUSDT', 'COMPUSDT', 'MANAUSDT', 'ANTUSDT', 'SANDUSDT', 'DOTUSDT', 'LUNAUSDT', 'RSRUSDT', 'KSMUSDT', 'EGLDUSDT', 'TRXUPUSDT', 'SUNUSDT', 'AVAXUSDT', 'HNTUSDT', 'AAVEUSDT', 'NEARUSDT',  'ROSEUSDT', 'AVAUSDT', 'AAVEUPUSDT', 'AAVEDOWNUSDT', 'SUSHIUPUSDT', 'SUSHIDOWNUSDT', '1INCHUSDT', 'REEFUSDT',  'SHIBUSDT', 'ICPUSDT', 'MASKUSDT',  'ATAUSDT', 'GTCUSDT', 'QNTUSDT','ENSUSDT', 'RNDRUSDT', 'SANTOSUSDT', 'APEUSDT', 'GALUSDT',  'LUNCUSDT', 'GMXUSDT',  'APTUSDT', 'HFTUSDT']

class Arbitrage():
    def __init__(self, root_exchange:Exchange) -> None:
        self.root_exchange = root_exchange # Serves as the bank and destination for all money        
        self.min_gap_percentage = 3
        self.max_gap_percentage = 15
        self.budget = 16
        self.budget_buffer = self.budget * 8
        

    def scan(self, exchange1:Exchange, exchange2:Exchange):                
        # TODO: hardcode list of symbols
        # currencies = exchange1.get_all_coins()        
        symbols = static_symbols
        # for currency in currencies:
        #     symbol = currency["symbol"]
        #     if symbol and "USDT" in symbol:
        #         symbols.append(symbol)        
        for symbol in symbols:
            print("Checking arbitrage for pair {} between exchanges {}/{}".format(symbol, exchange1.name(), exchange2.name()))
            # TODO: calculate transcations fees - each exchange take the fees as quntity from our order.
            result = self._should_take_arbitrage(exchange1, exchange2, symbol=symbol)
            if result: 
                self.write_to_file(result)
                print(result)                
                self.do(buy_exchange=result["BUY_EXCHANGE"], sell_exchange=result["SELL_EXCHANGE"],symbol=result["SYMBOL"],amount=float(result["COINS"]),funds=float(result["BUDGET"]))                                                
                return True
        return False

    def do(self, buy_exchange:Exchange, sell_exchange:Exchange, symbol, amount, funds):
        print("In do arbitrage with: buyExchange:{},sellExchange:{},symbol:{},amount:{},funds:{}\n".format(buy_exchange.name(),sell_exchange.name(),symbol,amount,funds))   
        amount =self._get_x_numbers_after_dot(amount)
        funds = self._get_x_numbers_after_dot(funds)        
        
        sell_exchange.create_margin_order(symbol=symbol,quantity=amount, funds=funds ,side=sell_exchange.side_sell())    
        try:                        
            buy_exchange.create_margin_order(symbol=symbol, quantity=amount, funds=funds, side=buy_exchange.side_buy()) 
        except Exception as e:
            print("In Do Arbitrage exception\n")
            print(e)
            # Buy the sold coins back
            sell_exchange.create_margin_order(symbol=symbol,quantity=amount, funds=funds, side=sell_exchange.side_buy()) 
            # TODO: repay loan
            raise Exception("Failed placing buy spot order, exchange:{},symbol:{},amount:{}\n err:{}".format(buy_exchange.name(),symbol,amount,e))
        

    def _calculate_gap_precentages(self, buy_orderbook, sell_orderbook):
        pass # TODO: return price gap percentages
    def _calculate_expected_profit(self, gap, amount, fees):
        expected_profit = (gap * amount) / 100
        return expected_profit - fees
    def _calculate_arbitrage_fees(self, buy_exchange, sell_exchange, symbol):
        # TODO: check buy_exchange balance and transfer money if needed
        pass # What's the cheapest network for this asset?
    def _calculate_transfer_time(self):
        pass  # TODO: calculate tansfer time (also if needed to transfer money to buy_exchange)
    def _check_budget_buffer(self, results):
        for result in results:
            if result["total_cost"] >= self.budget_buffer:
                return True
        return False

    def _calculate_arbitrage_volume(self, buy_orderbook, sell_orderbook, min_accepted_profit=None):        
        results = []                
        buy_index = sell_index = 0
        total_amount = total_cost = total_profit = 0
        while buy_index < len(buy_orderbook) and sell_index < len(sell_orderbook) and total_cost <= self.budget_buffer:            
            buy_leader_price = float(buy_orderbook[buy_index][0])
            buy_leader_amount = float(buy_orderbook[buy_index][1])
            sell_leader_price =  float(sell_orderbook[sell_index][0])
            sell_leader_amount = float(sell_orderbook[sell_index][1])
            gap_percentage = self._get_change(buy_leader_price, sell_leader_price)
            amount = min(buy_leader_amount, sell_leader_amount)            
            if buy_leader_amount > sell_leader_amount:                            
                buy_orderbook[buy_index][1] = buy_leader_amount - sell_leader_amount
                price = sell_leader_price
                sell_index += 1
            elif buy_leader_amount < sell_leader_amount:
                sell_orderbook[sell_index][1] = sell_leader_amount- buy_leader_amount
                price = buy_leader_price
                buy_index += 1
            else:
                price = buy_leader_price
                buy_index += 1
                sell_index += 1
            if gap_percentage < self.min_gap_percentage or gap_percentage >= self.max_gap_percentage:
                break         
            cost = price * amount
            total_amount += amount # TODO: convert amount to decimal
            total_cost += cost 
            total_profit += cost * gap_percentage / 100
            results.append({"total_cost":total_cost, "total_profit":total_profit, "total_amount":total_amount ,"percentage":gap_percentage, "price":price})            
                                
        # TODO: support calculating part of column, no need to take the whole column always        
        return results

    def _should_take_arbitrage(self, exchange1:Exchange, exchange2:Exchange, symbol):
        orderbook1 = exchange1.get_order_book(symbol)
        orderbook2 = exchange2.get_order_book(symbol)           
        if not orderbook1 or not orderbook2 or not exchange1.get_ask_order_book(orderbook1) or not exchange2.get_bid_order_book(orderbook2):
            print("No matching orderbook found for {} at exchanges {}/{}".format(symbol,exchange1.name(),exchange2.name()))
            return False
        volume = self._calculate_arbitrage_volume(buy_orderbook=exchange1.get_ask_order_book(orderbook1), sell_orderbook=exchange2.get_bid_order_book(orderbook2))
        if len(volume) > 0 and self._check_budget_buffer(volume):  # TODO: consider using total cost vaariable from should_take_arbitrage           
            return self.summary(symbol=symbol, buy_exchange=exchange1, sell_exchange=exchange2, volume=volume)                 

        volume = self._calculate_arbitrage_volume(buy_orderbook=exchange2.get_ask_order_book(orderbook2), sell_orderbook=exchange1.get_bid_order_book(orderbook1))
        if len(volume) > 0 and self._check_budget_buffer(volume):
            return self.summary(symbol=symbol, buy_exchange=exchange2, sell_exchange=exchange1, volume=volume)                        
            
        return None        

    def _get_change(self, num1, num2):
        big = max(num1, num2)
        small = min(num1, num2)
        return ((100 * big) / small) - 100

    def summary(self, symbol, buy_exchange:Exchange, sell_exchange:Exchange, volume):
        i = 0
        total_coins = 0        
        while i < len(volume) - 1 and volume[i + 1]["total_cost"] < self.budget: i+= 1
        total_coins = volume[i]["total_amount"]
        if total_coins * volume[i]["price"] >= self.budget:
            total_coins = self.budget / volume[i]["price"]
        else:
            remaning_dolars = self.budget - volume[i]["total_cost"]
            if remaning_dolars > 0:
                total_coins += remaning_dolars / volume[i + 1]["price"]        
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")                    
        return  {"TIME":current_time,"SYMBOL":symbol,"BUDGET":self.budget,"COINS":total_coins,"BUY_EXCHANGE":buy_exchange,"SELL_EXCHANGE":sell_exchange,"VOLUME":volume}

    def write_to_file(self,result):
        summary = copy.deepcopy(result)
        summary["BUY_EXCHANGE"] = summary["BUY_EXCHANGE"].name()
        summary["SELL_EXCHANGE"] = summary["SELL_EXCHANGE"].name()       
        with open("arbitrages.txt", "a") as myfile:
            myfile.write("\n")
            myfile.write(json.dumps(summary))
            myfile.write("\n")
        winsound.Beep(2500, 1000)    

    def _get_x_numbers_after_dot(self, number):
        if type(number) != float:
            raise Exception("_get_x_numbers_after_dot: only float numbers are accepted")
        if not number: return
        return float('{:.2f}'.format(number)) # TODO: solve binance LOT_SIZE issue that forced us to keep only 2 numbers after dot

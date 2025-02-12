import json
import copy
import time
# import winsound
from exchanges.exchanges import Exchange
from datetime import datetime
from services.send_email import sendEmail
from datetime import datetime

static_symbols =  ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'NEOUSDT', 'LTCUSDT', 'ADAUSDT', 'XRPUSDT', 'EOSUSDT', 'ONTUSDT', 'TRXUSDT', 'ETCUSDT', 'LINKUSDT', 'WAVESUSDT', 'ZILUSDT', 'ZECUSDT', 'DASHUSDT', 'NANOUSDT', 'THETAUSDT', 'ENJUSDT', 'MATICUSDT', 'ATOMUSDT', 'DOGEUSDT', 'DUSKUSDT','CHZUSDT', 'RVNUSDT', 'HBARUSDT', 'VITEUSDT', 'FTTUSDT', 'SOLUSDT', 'COMPUSDT', 'MANAUSDT', 'ANTUSDT', 'SANDUSDT', 'DOTUSDT', 'LUNAUSDT', 'RSRUSDT', 'KSMUSDT', 'EGLDUSDT', 'TRXUPUSDT', 'SUNUSDT', 'AVAXUSDT', 'HNTUSDT', 'AAVEUSDT', 'NEARUSDT',  'ROSEUSDT', 'AVAUSDT', 'AAVEUPUSDT', 'AAVEDOWNUSDT', 'SUSHIUPUSDT', 'SUSHIDOWNUSDT', '1INCHUSDT', 'REEFUSDT',  'SHIBUSDT', 'ICPUSDT', 'MASKUSDT',  'ATAUSDT', 'GTCUSDT', 'QNTUSDT','ENSUSDT', 'RNDRUSDT', 'SANTOSUSDT', 'APEUSDT', 'GALUSDT',  'LUNCUSDT',  'APTUSDT', 'HFTUSDT']
# IGNORE_ERROR_MESSAGES = ["The system does not have enough asset now", "Current symbol does not support margin trade", "Not a valid margin asset"]
IGNORE_ERROR_MESSAGES = []
IGNORE_LIST_PATH = "ignore_list.txt"

class Arbitrage():
    def __init__(self, root_exchange:Exchange) -> None:
        self.root_exchange = root_exchange # Serves as the bank and destination for all money        
        self.min_gap_percentage = 1
        self.max_gap_percentage = 15
        self.budget = 14
        self.budget_buffer = self.budget * 500
        self.ignore_list = self.read_ignore_list()
        
    def scan(self, symbols, exchange1:Exchange, exchange2:Exchange):               
        for symbol in symbols:
            if symbol in self.ignore_list:
                continue
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")   
            print("{} checking arbitrage for pair {} between exchanges {}/{}".format(current_time,symbol, exchange1.name(), exchange2.name()))
            # TODO: calculate transcations fees - each exchange take the fees as quntity from our order.
            # result = self._should_take_arbitrage(exchange1, exchange2, symbol=symbol)
            result = self._should_take_arbitrage(exchange1, exchange2, symbol=symbol)            
            if result: 
                self.write_to_file(result)
                print(result)                
                self.do(buy_exchange=result["BUY_EXCHANGE"], sell_exchange=result["SELL_EXCHANGE"],symbol=result["SYMBOL"],amount=float(result["COINS"]),funds=float(result["BUDGET"]))                                
                sendEmail(title="Do Arbitrage success",contect="Come take your money:\n{}".format(str(result)))
                return True
            time.sleep(0.03)
        return False

    def do(self, buy_exchange:Exchange, sell_exchange:Exchange, symbol, amount, funds): 
        amount =self._get_x_numbers_after_dot(amount)
        funds = self._get_x_numbers_after_dot(funds)
        print_data = "In do arbitrage with: buyExchange:{},sellExchange:{},symbol:{},amount:{},funds:{}\n".format(buy_exchange.name(),sell_exchange.name(),symbol,amount,funds)
        print(print_data)  
        is_sell_success = False
        try:                        
            is_sell_success = sell_exchange.create_margin_order(symbol=symbol,quantity=amount, funds=funds ,side=sell_exchange.side_sell()) 
            if is_sell_success: 
                is_buy_success = buy_exchange.create_margin_order(symbol=symbol, quantity=amount, funds=funds, side=buy_exchange.side_buy()) 
                if not is_buy_success:
                    raise Exception("Unexpected buy failure: this exepction is manually raised, {}".format(print_data))
        except Exception as e:            
            print("In Do Arbitrage exception\n")
            print(e)
            should_send_email = True
            for err_msg in IGNORE_ERROR_MESSAGES:
                if err_msg in str(e):
                    should_send_email = False
                    break
            if should_send_email:
                sendEmail(title="Do Arbitrage exception",contect="{}\n{}".format(print_data, str(e)))
            self.add_symbol_to_ignore_list(symbol)            
            # Buy the sold coins back
            if is_sell_success:
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

    def _calculate_arbitrage_volume(self, buy_orderbook, sell_orderbook):                        
        results = []                
        buy_index = sell_index = 0
        total_amount = total_cost = total_profit = 0        
        while buy_index < len(buy_orderbook) and sell_index < len(sell_orderbook) and total_cost <= self.budget_buffer:            
            buy_leader_price = float(buy_orderbook[buy_index][0])
            buy_leader_amount = float(buy_orderbook[buy_index][1])
            sell_leader_price =  float(sell_orderbook[sell_index][0])
            sell_leader_amount = float(sell_orderbook[sell_index][1])
            # gap_percentage = self._get_change(buy_leader_price, sell_leader_price)
            gap_percentage = self.bot_calculate_arbitrage_gap(buy_leader_price, sell_leader_price)
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

    def _calculate_arbitrage_volume2(self, buy_orderbook, sell_orderbook, budget_buffer , min_gap_percentage):
        """
        TODO:
        1. Calcualte how many coins can buy/sell at each platform using the input balance
        2. Calcualte how many spare coins you will gain
        3. Calcualte how much the spare coins worth in dollars
        4. Calcualte the profit in percentages
        """        
        buy_total_coins, last_buy_price = self._calculate_arbitrage_coins(buy_orderbook, budget_buffer, False)
        sell_total_coins, last_sell_price = self._calculate_arbitrage_coins(sell_orderbook, budget_buffer, True)
        coins_profit = buy_total_coins - sell_total_coins
        profit_dollars = coins_profit * last_sell_price
        profit_percentage = profit_dollars / budget_buffer * 100
        result = {"total_cost":self.budget, "total_profit":profit_dollars,"percentage":profit_percentage, "price":last_sell_price, "total_buy_coins":buy_total_coins, "total_sell_coins":sell_total_coins}
        print(result)
        if profit_percentage >= min_gap_percentage: 
            return [result]
        else:
            return []

    def _should_take_arbitrage2(self, exchange1:Exchange, exchange2:Exchange, symbol):
        orderbook1 = exchange1.get_order_book(symbol)
        orderbook2 = exchange2.get_order_book(symbol)           
        if not orderbook1 or not orderbook2 or not exchange1.get_ask_order_book(orderbook1) or not exchange2.get_bid_order_book(orderbook2):
            print("No matching orderbook found for {} at exchanges {}/{}".format(symbol,exchange1.name(),exchange2.name()))
            self.add_symbol_to_ignore_list(symbol)
            return False
        volume = self._calculate_arbitrage_volume2(buy_orderbook=exchange1.get_bid_order_book(orderbook1), sell_orderbook=exchange2.get_ask_order_book(orderbook2), budget_buffer=self.budget_buffer, min_gap_percentage=self.min_gap_percentage)
        if len(volume) > 0:  # TODO: consider using total cost vaariable from should_take_arbitrage           
           return volume              

        volume = self._calculate_arbitrage_volume2(buy_orderbook=exchange2.get_bid_order_book(orderbook2), sell_orderbook=exchange1.get_ask_order_book(orderbook1), budget_buffer=self.budget_buffer, min_gap_percentage=self.min_gap_percentage)
        if len(volume) > 0:
            return volume
            
        return None   

    def _should_take_arbitrage(self, exchange1:Exchange, exchange2:Exchange, symbol):
        orderbook1 = exchange1.get_order_book(symbol)
        orderbook2 = exchange2.get_order_book(symbol)           
        if not orderbook1 or not orderbook2 or not exchange1.get_ask_order_book(orderbook1) or not exchange2.get_bid_order_book(orderbook2):
            print("No matching orderbook found for {} at exchanges {}/{}".format(symbol,exchange1.name(),exchange2.name()))
            self.add_symbol_to_ignore_list(symbol)
            return False
        volume = self._calculate_arbitrage_volume(buy_orderbook=exchange1.get_bid_order_book(orderbook1), sell_orderbook=exchange2.get_ask_order_book(orderbook2))        
        if len(volume) > 0 and self._check_budget_buffer(volume):  # TODO: consider using total cost vaariable from should_take_arbitrage               
            return self.summary(symbol=symbol, buy_exchange=exchange1, sell_exchange=exchange2, volume=volume)                 

        volume = self._calculate_arbitrage_volume(buy_orderbook=exchange2.get_bid_order_book(orderbook2), sell_orderbook=exchange1.get_ask_order_book(orderbook1))
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
        #winsound.Beep(2500, 1000)   

    def add_symbol_to_ignore_list(self, symbol):
        self.ignore_list.append(symbol)
        with open(IGNORE_LIST_PATH, 'w') as f:
            for line in self.ignore_list:
                f.write("%s\n" % line)

    def read_ignore_list(self):        
        try:
            stopword=open(IGNORE_LIST_PATH,"r")
            lines = stopword.read().split('\n')
            # print("ignore list:\n {}".format(lines))
            return lines
        except Exception as e:
            print(e)
            return []

    def _get_x_numbers_after_dot(self, number):
        if type(number) != float:
            raise Exception("_get_x_numbers_after_dot: only float numbers are accepted")
        if not number: return
        return float('{:.2f}'.format(number)) # TODO: solve binance LOT_SIZE issue that forced us to keep only 2 numbers after dot

    def _calculate_arbitrage_coins(self, orderbook, balance, is_sell_orderbook):
        # if is_sell_orderbook:
        #     orderbook = orderbook[::-1]
        total_coins = 0
        index = 0
        price = None
        current_balance = balance        
        while index < len(orderbook) and current_balance > 0:
            price = float(orderbook[index][0])
            amount = float(orderbook[index][1])                        
            cost = price * amount            
            if current_balance >= cost:
                total_coins += amount                
            else:                
                total_coins += current_balance /  price
                cost = current_balance                
            current_balance -= cost
            index += 1            
        return total_coins, price

    def bot_calculate_arbitrage_gap(self, best_bid_1, best_ask_2):
        # Calculate the arbitrage gap percentage
        gap = (best_ask_2 - best_bid_1) / best_bid_1 * 100
        return gap

    def bot_calcualte_arbitrage_gap_with_budget(self,order_book_1, order_book_2, budget):                
        # Get the best bid and ask prices from both order books
        best_bid_1 = float(order_book_1["bids"][0][0])
        best_ask_1 = float(order_book_1["asks"][0][0])
        best_bid_2 = float(order_book_2["bids"][0][0])
        best_ask_2 = float(order_book_2["asks"][0][0])

        # Calculate the maximum number of units that can be bought and sold within the budget
        max_units_buy = budget / best_ask_1
        max_units_sell = budget / best_bid_2

        # Calculate the arbitrage gap percentage based on the maximum units that can be bought and sold
        gap = (best_ask_2 * max_units_sell - best_bid_1 * max_units_buy) / (best_bid_1 * max_units_buy) * 100
        return gap


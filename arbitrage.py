from exchanges.exchanges import Exchange

class Arbitrage():
    def __init__(self, root_exchange:Exchange) -> None:
        self.root_exchange = root_exchange # Serves as the bank and destination for all money
        self.max_balance = 10000
        

    def scan(self, exchange1:Exchange, exchange2:Exchange):                
        currencies = exchange1.get_all_coins()        
        symbols = []
        for currency in currencies:
            symbol = currency["symbol"]
            if symbol and "USDT" in symbol:
                symbols.append(symbol)
        
        print("Checking arbitrage for pair {} between exchanges {}/{}".format(symbol, exchange1.name(), exchange2.name()))
        result = self._should_take_arbitrage(exchange1, exchange2, symbol="BTCUSDT")            

    def do(self, buy_exchange:Exchange, sell_exchange:Exchange, symbol, amount):
        if not self._should_take_arbitrage(buy_exchange, sell_exchange, symbol, amount):
            print("Do arbitrage calcualted not profitable for symbol:{}".format(symbol))                          
        # TODO: ensure that both exchanges as the same network for this coin. so it can be transfered!! otherwise do it manually.        
        buy_exchange.create_order(symbol=symbol, quantity=amount, side=buy_exchange.side_buy)        
        dest_wallet = sell_exchange.get_deposit_address(symbol) # TODO: specify network
        buy_exchange.withdraw(asset=symbol, address=dest_wallet, amount=amount)
        # TODO: wait for coin to arrive - get history or check balance in loop.
        sell_exchange.create_order(symbol=symbol, quantity=amount, side=buy_exchange.side_sell)
        if sell_exchange.name != self.root_exchange.name:
            pass # TODO: transfer money back to root

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

    def _calculate_arbitrage_volume(self, buy_orderbook, sell_orderbook, min_accepted_profit=None):
        results = []
        buy_index = len(buy_orderbook) - 1
        sell_index = len(sell_orderbook) - 1
        gap_percentage = 100
        print("\nbuy order book:\n {}".format(buy_orderbook))
        print("\nsell order book:\n {}".format(sell_orderbook))
        while buy_index >= 0 and sell_index >= 0 :            
            buy_leader_price = float(buy_orderbook[buy_index][0])
            buy_leader_amount = float(buy_orderbook[buy_index][1])
            sell_leader_price =  float(sell_orderbook[sell_index][0])
            sell_leader_amount = float(sell_orderbook[sell_index][1])
            gap_percentage = self._get_change(buy_leader_price, sell_leader_price)
            amount = min(buy_leader_amount, sell_leader_amount)            
            if buy_leader_amount > sell_leader_amount:                            
                buy_orderbook[buy_index][1] = buy_leader_amount - sell_leader_amount
                price = sell_leader_price
                sell_index -= 1
            elif buy_leader_amount < sell_leader_amount:
                sell_orderbook[sell_index][1] = sell_leader_amount- buy_leader_amount
                price = buy_leader_price
                buy_index -= 1
            else:
                price = buy_leader_price
                buy_index -= 1
                sell_index -= 1
            results.append({"percentage":gap_percentage,"price":price,"amount":amount})        
        total_cost = total_profit = 0        
        profits_results = []
        # TODO: merge this logic with the while loop above
        i = 0
        cost = results[i]["price"] * results[i]["amount"] 
        # TODO: support calculating part of column, no need to take the whole column always.
        while i < len(results) - 1 and total_cost + cost <= self.max_balance:            
            total_cost += cost 
            total_profit += cost * results[i]["percentage"] / 100
            profits_results.append({"total_cost":total_cost, "total_profit":total_profit}) 
            i += 1
            cost = results[i]["price"] * results[i]["amount"]             
        print("\short nsummary:\n{}".format(profits_results))

        return 0       

    def _should_take_arbitrage(self, exchange1:Exchange, exchange2:Exchange, symbol):
        orderbook1 = exchange1.get_order_book(symbol)
        orderbook2 = exchange2.get_order_book(symbol)        
        if not orderbook1 or not orderbook2:            
            print("No matching orderbook found for {} at exchanges {}/{}".format(symbol,exchange1.name(),exchange2.name()))
            return False
        volume = self._calculate_arbitrage_volume(buy_orderbook=exchange1.get_ask_order_book(orderbook1), sell_orderbook=exchange2.get_bid_order_book(orderbook2))
        # volume = self._calculate_arbitrage_volume(buy_orderbook=exchange1.get_ask_order_book(orderbook2), sell_orderbook=exchange2.get_bid_order_book(orderbook1))
        # TODO: estimate if we have enough time to do all the transfers (maybe use coin volume staticts from past 24 hours)
        # if volume amount, transfer_time
        return False         
        gap = self._calculate_gap_precentages(buy_orderbook=buy_orderbook, sell_orderbook=sell_orderbook)
        fees = self._calculate_arbitrage_fees(buy_exchange, sell_exchange, symbol)
        profit = self._calculate_expected_profit(gap, amount, fees)
        return profit > 0

    def _get_change(self, num1, num2):
        big = max(num1, num2)
        small = min(num1, num2)
        return ((100 * big) / small) - 100

from exchanges.exchanges import Exchange

class Arbitrage():
    def __init__(self, root_exchange:Exchange) -> None:
        self.root_exchange = root_exchange # Serves as the bank and destination for all money
        
    def do(self, buy_exchange:Exchange, sell_exchange:Exchange, symbol, amount):
        if not self._should_take_arbitrage(buy_exchange, sell_exchange, symbol, amount):
            print("Do arbitrage calcualted not profitable for symbol:{}".format(symbol))
            return                
        # TODO: ensure that both exchanges as the same network for this coin. so it can be transfered!! otherwise do it manually.
        return
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
    def _calculate_arbitrage_volume(self, buy_orderbook, sell_orderbook):
        pass
    def _should_take_arbitrage(self, buy_exchange:Exchange, sell_exchange:Exchange, symbol, amount):
        buy_orderbook = buy_exchange.get_order_book(symbol)
        sell_orderbook = sell_exchange.get_order_book(symbol)
        volume = self._calculate_arbitrage_volume(buy_exchange, sell_exchange)
        gap = self._calculate_gap_precentages(buy_orderbook=buy_orderbook, sell_orderbook=sell_orderbook)
        fees = self._calculate_arbitrage_fees(buy_exchange, sell_exchange, symbol)
        profit = self._calculate_expected_profit(gap, amount, fees)
        return profit > 0 and volume > 2000

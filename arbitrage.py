from exchanges.exchanges import Exchange

class Arbitrage():
    def __init__(self) -> None:
        pass
    def do(buy_exchange:Exchange, sell_exchange:Exchange, symbol, amount):
        print(buy_exchange.get_order_book())
    

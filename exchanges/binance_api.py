from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
from binance.exceptions import BinanceAPIException

BINANCE_NAME = "BINANCE"

class BinanceAPI():
    def __init__(self, api_key, api_secret) -> None:
        self.client = Client(api_key, api_secret)
        print("Connected to binance API with permissions:\n{}".format(self.client.get_account_api_permissions()))

    def get_order_book(self, symbol):
        return self._get_order_book(symbol)

    def get_bid_order_book(self, orderbook):                
        return orderbook["bids"]

    def get_ask_order_book(self, orderbook):                
        return orderbook["asks"]

    def create_order(self, symbol, quantity ,side=Client.SIDE_BUY, type=Client.ORDER_TYPE_MARKET):                                
        return self.client.create_order(
                symbol=symbol,
                side=side,
                type=type,
                quantity=quantity)

    def withdraw(self, asset, address, amount):
        try:
            result = self.client.withdraw(
            asset=asset,
            address=address,
            amount=100)
        except BinanceAPIException as e:
            print(e)
        else:
            print("Withdraw success")

    def get_deposit_address(self, coin):
        return self.client.get_deposit_address(coin=coin)
    
    def get_all_coins(self):
        return self.client.get_all_tickers()

    def side_buy(self):
        return Client.SIDE_BUY
    
    def side_sell(self):
        return Client.SIDE_SELL    
    
    def name(self):
        return BINANCE_NAME

    def _get_order_book(self, symbol):
        return self.client.get_order_book(symbol=symbol)



from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
from binance.exceptions import BinanceAPIException

class BinanceAPI():
    def __init__(self, api_key, api_secret) -> None:
        self.client = Client(api_key, api_secret)

    def get_order_book(self, symbol="BTCUSDT"):
        return self.client.get_order_book(symbol=symbol)

    def create_order(self, symbol, quantity ,side=Client.SIDE_BUY, type=Client.ORDER_TYPE_MARKET):
        return self.client.create_test_order(
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



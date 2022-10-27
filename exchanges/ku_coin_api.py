from kucoin.client import Client

KU_COIN_NAME = "KUCOIN"

class KuCoinAPI():
    def __init__(self, api_key, api_secret, api_passphrase) -> None:
        self.client = Client(api_key, api_secret, api_passphrase)

    def get_order_book(self, symbol="BTCUSDT"):
        return self.client.get_order_book(symbol=symbol)

    def create_order(self, symbol, quantity ,side=Client.SIDE_BUY, type=None):
        return self.client.create_market_order(
                symbol=symbol,
                side=side,
                size=quantity)

    def withdraw(self, asset, address, amount):
        self.client.create_withdrawal(currency=asset, amount=amount, address=address)

    def get_deposit_address(self, coin):
        return self.client.get_deposit_address(coin=coin)
    
    def side_buy(self):
        return Client.SIDE_BUY

    def side_sell(self):
        return Client.SIDE_SELL

    def name(self):
        return KU_COIN_NAME


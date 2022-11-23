from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
from binance.exceptions import BinanceAPIException

BINANCE_NAME = "BINANCE"

class BinanceAPI():
    def __init__(self, api_key, api_secret) -> None:
        self.base_asset = "BUSD"
        self.client = Client(api_key, api_secret)
        self.balance = self.client.get_asset_balance(asset=self.base_asset)        
        print("Connected to binance API with {} balance: {}".format(self.base_asset, self.balance))

    def get_order_book(self, symbol):
        return self._get_order_book(symbol)

    def get_bid_order_book(self, orderbook):                
        return orderbook["bids"]

    def get_ask_order_book(self, orderbook):                
        return orderbook["asks"]

    def create_order(self, symbol, quantity ,side=Client.SIDE_BUY, type=Client.ORDER_TYPE_MARKET):  
        # Just remeber - “quantity” is used to describe base asset (left of the symbol) and “quoteOrderQty” for the quote(right) asset        
        return self.client.create_order(
                symbol=symbol,
                side=side,
                type=type,
                quantity=quantity)

    def transfer_spot_to_margin(self, amount=None, asset=None):      
        self.client.transfer_spot_to_margin(asset=asset or self.base_asset, amount=amount or self.balance) 
    
    def create_margin_order(self, symbol, quantity ,side=Client.SIDE_SELL, type=Client.ORDER_TYPE_MARKET):
        asset = symbol.split(self.base_asset)[0]        
        self.client.create_margin_loan(asset=asset,amount=quantity)
        self.client.create_margin_order(symbol=symbol,
                side=side,
                type=type,
                quantity=quantity)        
        return 

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



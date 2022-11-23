from abc import ABC, abstractmethod
from exchanges.binance_api import BinanceAPI
from exchanges.ku_coin_api import KuCoinAPI

class Exchange(ABC):
    @abstractmethod    
    def name(self):
        pass
    @abstractmethod
    def get_order_book(self, symbol):
         pass
    @abstractmethod
    def get_bid_order_book(self, orderbook):
        pass
    @abstractmethod
    def get_ask_order_book(self, orderbook):
         pass
    @abstractmethod
    def create_order(self, symbol, quantity ,side, type):
        pass
    @abstractmethod
    def create_margin_order(self, symbol, quantity ,side, type):
        pass
    @abstractmethod
    def withdraw(self, asset, address, amount):
        pass
    @abstractmethod
    def get_deposit_address(self, coin):
        pass
    @abstractmethod    
    def side_buy(self):
        pass
    @abstractmethod        
    def side_sell(self):
        pass
    @abstractmethod        
    def get_all_coins(self):
        pass
    @abstractmethod    
    def transfer_spot_to_margin(self, amount, asset=None):
        pass

exchanges_dict = {
    "BINANCE":BinanceAPI(api_key="EH7v7ZmnN2jZbZunNfr6rV4TiOExiTpeTeMEpjyAtvpejW7ZYaUX2hIsh9oDYE5y", api_secret="CafYiClvTrQ68Y7kkZMliUYQJzZS7OyaZzIYk7QPCWjoazVqWcPIIsAQfM4cRW3I"),
    "KUCOIN":KuCoinAPI(api_key="6359404c869bf00001a17ee5", api_secret="b133272a-4bc3-4036-bc4e-d35f80bdf1d8", api_passphrase="thisisrandoM15")
}
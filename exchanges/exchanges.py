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
    def create_order(self, symbol, quantity ,side, type):
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

exchanges_dict = {
    "BINANCE":BinanceAPI(api_key="mrVUYYhSsnAl0yq5pfOwQmXUGnhzkgMi4r9tnkSio0ofjWXDYUtqPrDitvM7JD27", api_secret="ke7yeU6lrnRqLw9mfCxW9lmcP4lPG4opLfEx4xVXcAONEQ5162NO1eAB7QeIWuig"),
    "KUCOIN":KuCoinAPI(api_key="6359404c869bf00001a17ee5", api_secret="b133272a-4bc3-4036-bc4e-d35f80bdf1d8", api_passphrase="thisisrandoM15")
}
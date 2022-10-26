from exchanges.binance_api import BinanceAPI
from exchanges.ku_coin_api import KuCoinAPI

def do_arbitrage()

if __name__ == "__main__":
    binance_api = BinanceAPI(api_key="mrVUYYhSsnAl0yq5pfOwQmXUGnhzkgMi4r9tnkSio0ofjWXDYUtqPrDitvM7JD27", api_secret="ke7yeU6lrnRqLw9mfCxW9lmcP4lPG4opLfEx4xVXcAONEQ5162NO1eAB7QeIWuig")
    ku_coin_api = KuCoinAPI(api_key="6359404c869bf00001a17ee5", api_secret="b133272a-4bc3-4036-bc4e-d35f80bdf1d8", api_passphrase="thisisrandoM15")
    # print("Binance:\n")
    # print(binance_api.get_order_book())
    print("KuCoin:\n")
    print(ku_coin_api.get_order_book())
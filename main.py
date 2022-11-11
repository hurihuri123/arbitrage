import time
from arbitrage import Arbitrage
from exchanges.exchanges import exchanges_dict

if __name__ == "__main__":
    arbitrage = Arbitrage(root_exchange=exchanges_dict["BINANCE"])
    while True:
        try:
            arbitrage.scan(exchanges_dict["BINANCE"], exchanges_dict["KUCOIN"]) 
        except Exception as e:
            print(e)
            time.sleep(1)
import time
from arbitrage import Arbitrage
from exchanges.exchanges import exchanges_dict, Exchange

if __name__ == "__main__":
    arbitrage = Arbitrage(root_exchange=exchanges_dict["BINANCE"])    
    binance:Exchange = exchanges_dict["BINANCE"]
    kucoin:Exchange = exchanges_dict["KUCOIN"]

    while True:
        try:
            did_took_arbitrage = arbitrage.scan(exchanges_dict["BINANCE"], exchanges_dict["KUCOIN"]) 
            if did_took_arbitrage:
                break
            time.sleep(5)
        except Exception as e:
            print(e)
            time.sleep(1)

    
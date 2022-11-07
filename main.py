from arbitrage import Arbitrage
from exchanges.exchanges import exchanges_dict


if __name__ == "__main__":
    arbitrage = Arbitrage(root_exchange=exchanges_dict["BINANCE"])    
    arbitrage.scan(exchanges_dict["BINANCE"], exchanges_dict["KUCOIN"])
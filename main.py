from arbitrage import Arbitrage
from exchanges.exchanges import exchanges_dict


if __name__ == "__main__":
    arbitrage = Arbitrage(root_exchange=exchanges_dict["BINANCE"])
    arbitrage.do(buy_exchange=exchanges_dict["BINANCE"], sell_exchange=exchanges_dict["KUCOIN"],symbol="BTCUSDT", amount=0.001)
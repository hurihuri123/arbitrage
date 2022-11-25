import time
from arbitrage import Arbitrage
from exchanges.exchanges import exchanges_dict, Exchange

if __name__ == "__main__":
    arbitrage = Arbitrage(root_exchange=exchanges_dict["BINANCE"])    
    binance:Exchange = exchanges_dict["BINANCE"]
    kucoin:Exchange = exchanges_dict["KUCOIN"]
    # Binance spot buy
    # binance.create_order("XRPUSDT",52,binance.side_sell())  
    # Binance margin sell
    # binance.transfer_spot_to_margin(asset="BUSD", amount=20)
    # binance.create_margin_order("XRPUSDT",quantity=1,side=binance.side_sell())  

    # KuCoin spot buy
    # kucoin.create_order("XRPUSDT", 13, binance.side_sell())  
    # KuCoin margin sell
    # kucoin.transfer_spot_to_margin(asset="USDT", amount=18)    
    # kucoin.create_margin_order(symbol="XRPUSDT",funds=1,side=binance.side_buy()) 
    while True:
        try:
            arbitrage.scan(exchanges_dict["BINANCE"], exchanges_dict["KUCOIN"]) 
        except Exception as e:
            print(e)
            time.sleep(1)
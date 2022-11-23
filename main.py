import time
from arbitrage import Arbitrage
from exchanges.exchanges import exchanges_dict, Exchange

if __name__ == "__main__":
    arbitrage = Arbitrage(root_exchange=exchanges_dict["BINANCE"])    
    binance:Exchange = exchanges_dict["BINANCE"]
    # binance.create_order("XRPUSDT",52,binance.side_sell())  # This is SPOT buy/sell example

    # Sell coin
    binance.transfer_spot_to_margin(asset="BUSD", amount=20)
    binance.create_margin_order("XRPBUSD",quantity=32,side=binance.side_sell()) 
    print("out")
    exit(1)    
    while True:
        try:
            arbitrage.scan(exchanges_dict["BINANCE"], exchanges_dict["KUCOIN"]) 
        except Exception as e:
            print(e)
            time.sleep(1)
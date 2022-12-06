import time
from arbitrage import Arbitrage
from exchanges.exchanges import exchanges_dict, Exchange
from services.send_email import sendEmail

if __name__ == "__main__":
    arbitrage = Arbitrage(root_exchange=exchanges_dict["BINANCE"])    
    binance:Exchange = exchanges_dict["BINANCE"]
    kucoin:Exchange = exchanges_dict["KUCOIN"]

    symbols = []
    currencies = binance.get_all_coins()             
    for currency in currencies:
        symbol = currency["symbol"]
        if symbol and "USDT" in symbol:
            symbols.append(symbol)   

    while True:
        try:
            did_took_arbitrage = arbitrage.scan(symbols=symbols, exchange1=exchanges_dict["BINANCE"], exchange2=exchanges_dict["KUCOIN"]) 
            if did_took_arbitrage:
                break
            time.sleep(5)
        except Exception as e:
            print(e)
            time.sleep(1)
    sendEmail(title="Exiting arbitrage program", contect="im out")
    print("exit program")


    
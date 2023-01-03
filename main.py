import time
import json
from arbitrage import Arbitrage
from exchanges.exchanges import exchanges_dict, Exchange
from services.send_email import sendEmail

if __name__ == "__main__":
    arbitrage = Arbitrage(root_exchange=exchanges_dict["BINANCE"])    
    binance:Exchange = exchanges_dict["BINANCE"]
    kucoin:Exchange = exchanges_dict["KUCOIN"]

    

    # symbol = "KMDUSDT"
    # print("BINANCE ORDER BOOK:\n")
    
    # orderbook1 = binance.get_order_book(symbol)
    # orderbook2 = kucoin.get_order_book(symbol)  
    # print(arbitrage.bot_calcualte_arbitrage_gap_with_budget(orderbook1, orderbook2, 15))
    


    # with open('binance_orderbook.txt', 'w') as convert_file:
    #         convert_file.write(json.dumps(orderbook1))
    
    # with open('kucoin_orderbook.txt', 'w') as convert_file:
    #         convert_file.write(json.dumps(orderbook2))

    # print("ALGO 1 \n")
    # volume1 = arbitrage._should_take_arbitrage(binance,kucoin,symbol)
    # print(volume1)
    # volume2 = arbitrage._should_take_arbitrage(kucoin, binance,symbol)    
    # print(volume2)
    # print("ALGO 2 \n")
    # print(arbitrage._should_take_arbitrage2(binance,kucoin,symbol))


    # print("KUCOIN ORDER BOOK:\n")
    # print(kucoin.get_order_book())
    
    # print(arbitrage.temp_shuld_take_arbitrage(binance,kucoin,symbol))
    # print("algo 2")
    # print(arbitrage.temp_shuld_take_arbitrage2(binance,kucoin,symbol))

    binance_margin_symbols = ['BNBUSDT', 'BTCUSDT', 'ETHUSDT', 'TRXUSDT', 'XRPUSDT', 'EOSUSDT', 'LINKUSDT', 'ONTUSDT', 'ADAUSDT', 'ETCUSDT', 'LTCUSDT', 'XLMUSDT', 'XMRUSDT', 'NEOUSDT', 'ATOMUSDT', 'DASHUSDT', 'ZECUSDT', 'MATICUSDT', 'BATUSDT', 'IOSTUSDT', 'VETUSDT', 'QTUMUSDT', 'IOTAUSDT', 'XTZUSDT', 'BCHUSDT', 'RVNUSDT', 'BUSDUSDT', 'ZILUSDT', 'ONEUSDT', 'ANKRUSDT', 'TFUELUSDT', 'IOTXUSDT', 'HBARUSDT', 'FTMUSDT', 'SXPUSDT', 'DOTUSDT', 'ALGOUSDT', 'THETAUSDT', 'COMPUSDT', 'KNCUSDT', 'KAVAUSDT', 'DOGEUSDT', 'WAVESUSDT', 'MKRUSDT', 'SNXUSDT', 'CRVUSDT', 'SUSHIUSDT', 'UNIUSDT', 'MANAUSDT', 'JSTUSDT', 'AVAXUSDT', 'NEARUSDT', 'FILUSDT', 'TRBUSDT', 'RSRUSDT', 'AAVEUSDT', 'SANDUSDT', 'CHZUSDT', 'ARPAUSDT', 'COTIUSDT', 'FETUSDT', 'TROYUSDT', 'CHRUSDT', 'NMRUSDT', 'GRTUSDT', 'STPTUSDT', 'LRCUSDT', 'KSMUSDT', 'ROSEUSDT', 'REEFUSDT', 'STXUSDT', 'ENJUSDT', 'RUNEUSDT', 'SKLUSDT', 'INJUSDT', 'OGNUSDT', 'EGLDUSDT', '1INCHUSDT', 'DODOUSDT', 'LITUSDT', 'CAKEUSDT', 'SOLUSDT', 'LINAUSDT', 'MDXUSDT', 'SUPERUSDT', 'GTCUSDT', 'PUNDIXUSDT', 'AUDIOUSDT', 'BONDUSDT', 'SLPUSDT', 'POLSUSDT', 'PONDUSDT', 'NULSUSDT', 'TVKUSDT', 'ATAUSDT', 'DENTUSDT', 'ERNUSDT', 'ARUSDT', 'DYDXUSDT', 'UNFIUSDT', 'AXSUSDT', 'LUNAUSDT', 'SHIBUSDT', 'WINUSDT', 'ENSUSDT', 'ALICEUSDT', 'TLMUSDT', 'ICPUSDT', 'C98USDT', 'FLOWUSDT', 'BAKEUSDT', 'GALAUSDT', 'HIVEUSDT', 'DARUSDT', 'IDEXUSDT', 'MBOXUSDT', 'ANTUSDT', 'CLVUSDT', 'WAXPUSDT', 'KLAYUSDT', 'MINAUSDT', 'RNDRUSDT', 'JASMYUSDT', 'QUICKUSDT', 'LPTUSDT', 'AGLDUSDT', 'BICOUSDT', 'CTXCUSDT', 'DUSKUSDT', 'HOTUSDT', 'SFPUSDT', 'YGGUSDT', 'FLUXUSDT', 'ICXUSDT', 'CELOUSDT', 'BETAUSDT', 'BLZUSDT', 'MTLUSDT', 'PEOPLEUSDT', 'QNTUSDT', 'PYRUSDT', 'SUNUSDT', 'KEYUSDT', 'PAXGUSDT', 'WANUSDT', 'TWTUSDT', 'RADUSDT', 'QIUSDT', 'GMTUSDT', 'APEUSDT', 'KDAUSDT', 'MBLUSDT', 'API3USDT', 'CTKUSDT', 'NEXOUSDT', 'WOOUSDT', 'ASTRUSDT', 'GALUSDT', 'OPUSDT', 'REIUSDT', 'LEVERUSDT', 'LDOUSDT', 'FIDAUSDT', 'KMDUSDT', 'FLMUSDT', 'BURGERUSDT', 'AUCTIONUSDT', 'FIOUSDT', 'IMXUSDT', 'SPELLUSDT', 'STGUSDT', 'BELUSDT', 'WINGUSDT', 'AVAUSDT', 'DEXEUSDT', 'LUNCUSDT', 'SANTOSUSDT', 'EPXUSDT', 'HARDUSDT', 'DEGOUSDT', 'HIGHUSDT', 'GMXUSDT', 'LAZIOUSDT', 'PORTOUSDT', 'ACHUSDT', 'STRAXUSDT', 'FORTHUSDT', 'KP3RUSDT', 'BSWUSDT', 'REQUSDT', 'POLYXUSDT', 'APTUSDT', 'DATAUSDT', 'PHAUSDT', 'OSMOUSDT', 'GLMRUSDT', 'MASKUSDT']
    # currencies = binance.get_all_coins()             
    # for currency in currencies:
    #     symbol = currency["symbol"]
    #     if symbol and "USDT" in symbol:
    #         symbols.append(symbol)   

    while True:
        try:
            did_took_arbitrage = arbitrage.scan(symbols=binance_margin_symbols, exchange1=exchanges_dict["BINANCE"], exchange2=exchanges_dict["KUCOIN"]) 
            if did_took_arbitrage:
                break
            time.sleep(5)
        except Exception as e:
            print(e)
            time.sleep(1)
    sendEmail(title="Exiting arbitrage program", contect="im out")
    print("exit program")


    
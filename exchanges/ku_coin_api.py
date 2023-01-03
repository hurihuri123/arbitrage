from kucoin.client import Client

KU_COIN_NAME = "KUCOIN"

class KuCoinAPI():
    def __init__(self, api_key, api_secret, api_passphrase) -> None:
        self.client = Client(api_key, api_secret, api_passphrase)

    def get_order_book(self, symbol):
        symbol = self._format_symbol(symbol)
        return self._get_order_book(symbol)

    def get_bid_order_book(self, orderbook):        
        return orderbook["bids"]

    def get_ask_order_book(self, orderbook):                
        return orderbook["asks"]

    def create_order(self, symbol, quantity ,side, type=None):
        symbol = self._format_symbol(symbol)     
        return self.client.create_market_order(
                symbol=symbol,
                side=side,
                size=quantity)

    def transfer_spot_to_margin(self, amount, asset=None):
        self.client.create_inner_transfer(currency=asset, from_type="trade", to_type="margin", amount=amount)

    def create_margin_order(self, symbol, side, quantity=None, funds=None, order_type=None):
        print("In KuCoin side:{} symbol:{},quantity:{},funds:{},type:{}".format(side,symbol,quantity,funds,order_type))
        symbol = self._format_symbol(symbol)  
        if side == "BUY" or side == "buy":
            side = self.client.SIDE_BUY
            quantity = None            
        else:            
            side = self.client.SIDE_SELL
            funds = None                               
        response = self.client.create_margin_market_order(
                symbol=symbol,
                side=side,
                size=quantity,
                funds=funds                
                )        
        success = "orderId" in response and len(str(response["orderId"])) > 0
        if not success:
            raise Exception("KUCOIN: Failed openning margin order side:{}, type:{}, quantity:{}, funds:{}".format(side,order_type,quantity,funds))
        print("KuCoin {} {} success".format(side,symbol))
        return True

    def withdraw(self, asset, address, amount):
        self.client.create_withdrawal(currency=asset, amount=amount, address=address)

    def get_deposit_address(self, coin):
        return self.client.get_deposit_address(coin=coin)

    def get_all_coins(self):
        return self.client.get_currencies()
    
    def side_buy(self):
        return self.client.SIDE_BUY

    def side_sell(self):
        return self.client.SIDE_SELL

    def name(self):
        return KU_COIN_NAME

    def _format_symbol(self,symbol):
        splited = symbol.split("USDT")
        return splited[0] + "-USDT"

    def _get_order_book(self, symbol):
        return self.client.get_order_book(symbol=symbol)


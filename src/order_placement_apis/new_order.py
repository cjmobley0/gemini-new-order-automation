import datetime
import time
from utils.gemini_requests import GemRequests


class NewOrder(GemRequests):
    """ REST API Wrapper for Order Placement API's: New Order"""
    def __init__(self,
                 symbol: str,
                 amount: str,
                 price: str,
                 side: str,
                 type: str,
                 min_amount: str = None,
                 client_order_id: str = None,
                 options: list = None,
                 stop_price: str = None,
                 account: [str, bool] = None):

        # Payload Variables
        self.request = "/v1/order/new"
        self.nonce = str(int((time.mktime(datetime.datetime.now().timetuple()) * 1000)
                         + float(str(datetime.datetime.now().microsecond)[0:3])))
        self.client_order_id = client_order_id
        self.symbol = symbol
        self.amount = amount
        self.min_amount = min_amount
        self.price = price
        self.side = side
        self.type = type
        self.options = options
        self.stop_price = stop_price
        self.account = account
        super().__init__()

    def new_order_post(self, payload: [dict] = None, headers: [dict] = None):
        if not payload:
            payload = self.json()

        return self.post(endpoint=self.request, payload=payload, headers=headers)

    def json(self):
        """ Return Payload json/dict if values is not Empty/None"""
        temp_dict = self.__dict__
        return {k: v for k, v in temp_dict.items() if v}


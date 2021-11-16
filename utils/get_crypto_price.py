import datetime
import time
import requests
import json
import base64
import hmac
import hashlib
from utils.config import GEMINI_BASE_URL, GEMINI_API_KEY, GEMINI_API_SECRET


def get_crypto_price(symbol: str):
    nonce = str(int((time.mktime(datetime.datetime.now().timetuple()) * 1000)
                    + float(str(datetime.datetime.now().microsecond)[0:3])))
    payload = {
        "request": "/v1/instant/quote",
        "nonce": nonce,
        "symbol": symbol,
        "side": "sell",
        "totalSpend": "1"
    }

    encoded_payload = json.dumps(payload).encode()
    b64 = base64.b64encode(encoded_payload)
    signature = hmac.new(GEMINI_API_SECRET.encode(), b64, hashlib.sha384).hexdigest()

    request_headers = {'Content-Type': "text/plain",
                       'Content-Length': "0",
                       'X-GEMINI-APIKEY': GEMINI_API_KEY,
                       'X-GEMINI-PAYLOAD': b64,
                       'X-GEMINI-SIGNATURE': signature,
                       'Cache-Control': "no-cache"}

    response = requests.post(url=GEMINI_BASE_URL + payload.get('request'),
                             data=None,
                             headers=request_headers)
    response_json = response.json()
    return response_json.get('price')

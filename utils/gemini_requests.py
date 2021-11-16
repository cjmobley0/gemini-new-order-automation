"""
Gemini Python Request Module Wrapper

"""
import requests
import json
import base64
import hmac
import hashlib
from utils.config import GEMINI_API_KEY, GEMINI_API_SECRET, GEMINI_BASE_URL


class GemRequests:

    def __init__(self):
        self._gemini_signature = None
        self._headers = None
        self._payload = None
        self.api_key = GEMINI_API_KEY
        # self.payload_dict = None
        # self.payload_b64 = None
        self.status_code = None
        self.error_reason = None

    @property
    def gemini_signature(self):
        if not self._gemini_signature:
            return hmac.new(GEMINI_API_SECRET.encode(), self._payload, hashlib.sha384).hexdigest()

        return self._gemini_signature

    @gemini_signature.setter
    def gemini_signature(self, signature):
        self._gemini_signature = signature

    @property
    def payload(self):
        # Payload property call at the end will convert to b64
        if type(self._payload) is dict:
            # Convert payload dict to b64
            encoded_payload = json.dumps(self._payload).encode()
            self._payload = base64.b64encode(encoded_payload)
            return base64.b64encode(encoded_payload)

        return self._payload

    @payload.setter
    def payload(self, payload):
        self._payload = payload

    @property
    def headers(self):
        # Pull updated header values on each property call
        return {
            "Content-Type": "text/plain",
            "Content-Length": "0",
            "X-GEMINI-APIKEY": self.api_key,
            "X-GEMINI-PAYLOAD": self.payload,
            "X-GEMINI-SIGNATURE": self.gemini_signature,
            "Cache-Control": "no-cache"
        }

    @staticmethod
    def set_error_reason(response_text):
        try:
            return json.loads(response_text).get('reason')
        except:
            return None
        finally:
            pass

    def post(self,
             endpoint: str,
             payload: dict,
             headers: dict = None,
             data: [dict, str] = None):

        self._payload = payload

        if headers:  # Allow overriding of existing default headers
            self._headers = headers
            response = requests.post(url=GEMINI_BASE_URL + endpoint, data=data, headers=headers)
        else:
            response = requests.post(url=GEMINI_BASE_URL + endpoint, data=data, headers=self.headers)

        # response = requests.post(url=GEMINI_BASE_URL + endpoint, data=data, headers=self.headers)
        self.status_code = response.status_code
        self.error_reason = self.set_error_reason(response.text)

        return response



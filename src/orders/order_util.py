import requests
import json


def translate_to_order(text):
    # TODO suppr bouchon, évol...
    x = '{}'
    if "achète" in text:
        x = '{"pair":"XETHZEUR", "type":"buy", "ordertype":"market", "volume":1}'
    elif "vend" in text:
        x = '{"pair":"XETHZEUR", "type":"sell", "ordertype":"market", "volume":1}'
    y = json.loads(x)
    return y


def post_order(order, connected):
    if connected:
        r = requests.post("http://127.0.0.1:3000/order", data=order)
        return r
    return "pas connecté à kraken"

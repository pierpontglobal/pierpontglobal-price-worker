import websocket
import json
import PriceWorker
import requests
import os
import logging

try:
    import thread
except ImportError:
    import _thread as thread
import time


def on_message(ws, message):
    data = json.loads(message)
    try:
        data_message = json.loads(data['message'])
        action = data_message['action']
        print data['message']
        if (action == "query_mmr"):
            priceWorker.get_mmr(data_message, ws)
    except Exception, e:
        None


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("### closed ###")


def get_token():
    url = os.environ['IDENTITY_URL'] + "/oauth/token"

    payload = "{\"username\": \"" + os.environ['USERNAME'] + "\",\"password\": \"" + \
        os.environ['PASSWORD'] + "\",\"grant_type\": \"password\"}"
    headers = {
        'Content-Type': "application/json",
    }

    response = requests.request("POST", url, data=payload, headers=headers)
    return json.loads(response.text)['access_token']


def on_open(ws):
    def run(*args):
        data = {}
        data["command"] = "subscribe"
        data["identifier"] = "{\"channel\": \"PriceQueryChannel\"}"
        string_data = json.dumps(data)
        print 'Connecting to: ' + string_data
        ws.send(string_data)
    thread.start_new_thread(run, ())


if __name__ == "__main__":
    logging.debug('Starting price worker')
    token = get_token()
    priceWorker = PriceWorker.PriceWorker()

    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(os.environ['WEB_SOCKET_URL'] + "/cable?token=" + token,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    while True:
        ws.run_forever()
        time.sleep(3)

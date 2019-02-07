import websocket
import json
import PriceWorker

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
    except Exception,e: None

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

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
    priceWorker = PriceWorker.PriceWorker()

    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://api.pierpontglobal.com/cable?token=63dfd03b8c2a3bab112495489c64dcf92205a9d73449b3ca5c02132e6d08ddee",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    while True:
        ws.run_forever()
        time.sleep(3)
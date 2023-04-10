import json
import subprocess
import zmq
import os
from ai1.NLToJson import NLToJson

#
BinDir = os.getenv("NlspBinDir")
QCache = {}  # Initialize cache for queries


def stockdbsymfilter(date: str, expr: str) -> list:
    process = subprocess.run([BinDir + '/stockdbsymfilter', date, expr],
                             stdout=subprocess.PIPE, text=True)
    symbols = process.stdout.split('\n')
    return symbols[:-1]  # Remove the last empty element


def NLToSymWorker(addr_rep, multi_worker=False):
    """
    a function that creates a ZeroMQ REP socket, listens for incoming messages, and performs the following operations:
        1. Receives a message in the format {"q": "some q"} from the socket
        2. Passes the received q to the NLToJson function, which converts the q into a JSON formatted string {"Date": "some date", "Expr": "some expression"}
        3. Parses the JSON string
        4. Passes the date and expression to the C++ executable 'stockdbsymfilter', which returns a list of symbols
        5. Returns the list of symbols to the REP socket as a response
        6. Continues listening for new messages

    The function runs in an infinite loop, constantly listening for incoming messages and processing them as described.
    """
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    # connect instead of bind when using Broker
    if multi_worker:
        socket.connect(addr_rep)
    else:
        socket.bind(addr_rep)

    while True:
        q = socket.recv_string()

        # Check if q exists in cache, otherwise convert q to JSON
        if q in QCache:
            js_str = QCache[q]
            js = json.loads(js_str)
        else:
            try:
                js_str = NLToJson(q)
                js = json.loads(js_str)
                # Cache the JSON string only if parsable
                QCache[q] = js_str
            except Exception as e:
                socket.send_json({"error": "q_parse", "msg": js_str})
                continue

        # Check if JSON has keys 'Date' and 'Expr'
        if 'Date' not in js or 'Expr' not in js:
            socket.send_json({"error": "q_parse", "msg": js_str})
            continue
        date = js.get('Date')
        expr = js.get('Expr')

        # Convert JSON to symbols
        try:
            symbols = stockdbsymfilter(date, expr)
        except Exception as e:
            socket.send_json({"error": "db_query", "Date": date, "Expr": expr})
            continue

        response = {'symbols': symbols}
        socket.send_json(response)


if __name__ == '__main__':
    NLToSymWorker("ipc:///tmp/nl2sym.ipc")

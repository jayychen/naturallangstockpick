import json
import subprocess
import zmq
from ai1.NLToJson import NLToJson

#
QCache = {}  # Initialize cache for queries


def stockdbsymfilter(date: str, expr: str) -> list:
    """
    make sure folder containing stockdbsymfilter is in PATH
    """
    process = subprocess.run(['stockdbsymfilter', date, expr],
                             stdout=subprocess.PIPE, text=True)
    # Check if the command executed successfully
    if process.returncode != 0:
        raise RuntimeError(
            f"stockdbsymfilter command failed with return code {process.returncode}")

    symbols = process.stdout.split('\n')
    return symbols[:-1]  # Remove the last empty element


def NLToSymWorker(addr_rep, addr_log, multi_worker=False):
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
    # logger init
    ctx_log = zmq.Context()
    skt_log = ctx_log.socket(zmq.PUB)
    skt_log.connect(addr_log)

    while True:
        q = socket.recv_string()
        skt_log.send_json({'q': q})

        # Check if q exists in cache, otherwise convert q to JSON
        if q in QCache:
            js_str = QCache[q]
        else:
            js_str = NLToJson(q)
            QCache[q] = js_str

        # Convert gpt output to JSON
        try:
            js = json.loads(js_str)
            date = js.get('Date')
            expr = js.get('Expr')
        except Exception as e:
            # print error message
            print("Error: " + str(e))
            socket.send_json({"error": "gpt", "msg": js_str})
            skt_log.send_json({"error": "gpt", "msg": js_str})
            continue
        else:
            skt_log.send_string(js_str)

        # Convert JSON to symbols
        try:
            symbols = stockdbsymfilter(date, expr)
        except Exception as e:
            socket.send_json({"error": "db_query", "msg": {
                "Date": date, "Expr": expr}})
            skt_log.send_json({"error": "db_query", "msg": {
                "Date": date, "Expr": expr}})
            continue

        response = {'results': 'ok', 'symbols': symbols}
        socket.send_json(response)
        skt_log.send_json(response)


if __name__ == '__main__':
    NLToSymWorker("ipc:///tmp/nl2sym.ipc", "ipc:///tmp/nl2sym_log.ipc")

import json
import subprocess
import zmq
from ai1.NLToJson import NLToJson

#
PreQCache = {
    "volume increase 10 folds today vs previous 5 days":
    '{"Date":"today", "Expr": "qlmt(t=day)/qlmt(t=day,n=5,s=mean)>10"}',
    "random question":
    "I'm sorry, I didn't understand your question. Please provide a valid question related to the format of the JSON output."
}
ExploreID = 0
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


def stockdblastdate() -> str:
    """
    get the last date in the database
    """
    process = subprocess.run(['stockdblastdate'],
                             stdout=subprocess.PIPE, text=True)
    dat = process.stdout.split('\n')
    return dat[0]


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
        info = ""
        if q == 'explore':
            global ExploreID
            q = list(PreQCache.keys())[ExploreID]
            ExploreID = (ExploreID + 1) % len(PreQCache)
            info += f"Exploring: {q}\n"
        else:
            info += f"Checking: {q}\n"
        skt_log.send_json({'q': q})

        # Check if q exists in cache, otherwise convert q to JSON
        if q in PreQCache:
            js_str = PreQCache[q]
        elif q in QCache:
            js_str = QCache[q]
        else:
            try:
                js_str = NLToJson(q)
            except Exception as e:
                msg = {"error": "gpt", "msg": "can't connect to openai api"}
                socket.send_json(msg)
                skt_log.send_json(msg)
                continue
            QCache[q] = js_str

        # Convert gpt output to JSON
        try:
            js = json.loads(js_str)
            date = js.get('Date')
            if date == "today":
                date = stockdblastdate()
                info += f"Last available data on: {date}\n"
            expr = js.get('Expr')
        except Exception as e:
            resp = {"result": "error",
                    "err_msg": f"OpenAI: {js_str}"}
            skt_log.send_json(resp)
            if info != "":
                resp['info'] = info
            socket.send_json(resp)
            continue
        else:
            skt_log.send_string(js_str)

        # Convert JSON to symbols
        try:
            symbols = stockdbsymfilter(date, expr)
        except Exception as e:
            resp = {"result": "error",
                    "err_msg": f"DB Query failed for Date: {date}, Expr: {expr}"}
            skt_log.send_json(resp)
            if info != "":
                resp['info'] = info
            socket.send_json(resp)
            continue

        # success
        resp = {'result': 'ok', 'symbols': symbols}
        if info != "":
            resp['info'] = info
        socket.send_json(resp)
        skt_log.send_json(resp)


if __name__ == '__main__':
    NLToSymWorker("ipc:///tmp/nl2sym.ipc", "ipc:///tmp/nl2sym_log.ipc")

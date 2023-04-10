import sys
import zmq


def zmq_req_socket(addr_req: str, msg: str):
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect(addr_req)

    socket.send_string(msg)
    response = socket.recv_string()
    print(response)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python zmq_req_script.py <address> <message>")
        sys.exit(1)

    addr_req = sys.argv[1]
    msg = sys.argv[2]

    zmq_req_socket(addr_req, msg)

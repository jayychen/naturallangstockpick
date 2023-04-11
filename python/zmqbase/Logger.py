import zmq
from datetime import datetime


def zmq_sub_logger(addr_log: str, fname: str):
    '''
    zmq sub socket to log messages to file
    '''
    ctx_log = zmq.Context()
    skt_log = ctx_log.socket(zmq.SUB)
    skt_log.bind(addr_log)
    skt_log.subscribe('')

    with open(fname, 'a') as log_file:
        while True:
            try:
                msg = skt_log.recv_string()
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                log_file.write(f'{timestamp} {msg}\n')
                log_file.flush()
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Error occurred: {e}")
                break
    skt_log.close()
    ctx_log.term()

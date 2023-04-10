import threading
import argparse
from zmqbase.Hub import Broker
from ai1.NLToSym import NLToSymWorker


def start_workers(nworkers: int, addr_dealer: str):
    workers = []
    for _ in range(nworkers):
        worker = threading.Thread(
            target=NLToSymWorker, args=(addr_dealer, True))
        worker.start()
        workers.append(worker)
    return workers


if __name__ == '__main__':
    # arguements
    parser = argparse.ArgumentParser(
        description="Start the Natural Language to Symbol Vec multi-worker service.")
    parser.add_argument('--addr', default="ipc:///tmp/nl2sym_service.ipc",
                        help="Address for the ROUTER socket (default: ipc:///tmp/nl2sym_service.ipc)")
    parser.add_argument('--nworker', type=int, default=1,
                        help="Number of worker threads (default: 1)")
    args = parser.parse_args()

    if args.nworker == 1:
        NLToSymWorker(args.addr)
    else:
        addr_dealer = "ipc:///tmp/nl2sym_dealer.ipc"
        broker = threading.Thread(
            target=Broker, args=(args.addr, addr_dealer))
        broker.start()

        workers = start_workers(args.nworker, addr_dealer)

        broker.join()  # The broker thread will run indefinitely, so the script won't exit

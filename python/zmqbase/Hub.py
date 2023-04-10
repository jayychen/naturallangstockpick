import zmq


def Broker(addr_router, addr_dealer, context: zmq.Context = None):
    """
    used when having N REQ and N REP
    """
    context = context or zmq.Context.instance()

    # Socket facing clients
    frontend = context.socket(zmq.ROUTER)
    frontend.bind(addr_router)

    # Socket facing services
    backend = context.socket(zmq.DEALER)
    backend.bind(addr_dealer)

    zmq.proxy(frontend, backend)

    # never get here...
    frontend.close()
    backend.close()
    context.term()

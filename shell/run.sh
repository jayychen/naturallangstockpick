#!/bin/bash
function startNLSPService() {
  python3.8 -m ai1.service $@
}

function stopNLSPService() {
  kill_proc_with_kw "python3.8 -m ai1.service"
}

function utNLSPService() {
  python3.8 -m zmqbase.ut_zmq_req "ipc:///tmp/nl2sym_service.ipc" "volume increse 10 folds today vs previous 5 days on 2023-04-03"
}
const express = require('express');
const { Server } = require('socket.io');
const zmq = require('zeromq');
const http = require('http');

const app = express();
const server = http.createServer(app);
const io = new Server(server);

app.use(express.static('public'));

var zmq_req = zmq.socket('req');
zmq_req.connect('ipc:///tmp/nl2sym_service.ipc');



io.on('connection', (socket) => {
  console.log('A user connected');

  //receive question from client
  socket.on('submitQuestion', (data) => {
    forwardRequestToZeroMQ(data)
      .then((response) => {
        console.log("response", JSON.stringify(response));
        socket.emit('response', response);
      })
      .catch((error) => {
        console.log("error", JSON.stringify(error));
        socket.emit('response', error);
      });
  });

  socket.on('disconnect', () => {
    console.log('A user disconnected');
  });
});

function forwardRequestToZeroMQ(data) {
  return new Promise((resolve, reject) => {
    console.log(JSON.stringify(data));
    zmq_req.send(data['question']);
    zmq_req.on('message', (response) => {
      resolve(JSON.parse(response));
    });

    zmq_req.on('error', (error) => {
      reject(error);
    });
  });
}

const PORT = process.env.PORT || 3000;
server.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});

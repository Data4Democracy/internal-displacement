'use strict';

const express = require("express");
const http = require('http');
const env = process.env.NODE_ENV || 'development';
// Setup server
const app = express();
const server = http.createServer(app);
require('./routes')(app);

app.set('port', (process.env.PORT || 3322));

if (process.env.NODE_ENV === 'production') {
    app.use(express.static('client/build'));
}

function startServer() {
    server.listen(app.get('port'), () => {
        console.log('Express server listening on %d, in %s mode', app.get('port'), env);
    });
}

setImmediate(startServer);





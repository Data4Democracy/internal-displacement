const pgp = require('pg-promise')();
let connectionObj;
//if not using docker
//create a pgConfig.js file in the same directory and put your credentials there
if (process.env.NODE_DB === 'LOCAL') {
    connectionObj = require('./pgConfig');
} else {
    connectionObj = {
        user: process.env.DB_USER,
        database: process.env.DB_NAME,
        password: process.env.DB_PASS,
        host: process.env.DB_HOST
    };
}

//export db instance to be shared
module.exports = pgp(connectionObj);

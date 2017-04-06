const pgp = require('pg-promise')();
const connectionObj = {
    host: 'localhost',
    port: 5432,
    database: 'id_test',
    user: 'wwymak',
    password: 'wwymak'
};

//export db instance to be shared
module.exports = pgp(connectionObj);

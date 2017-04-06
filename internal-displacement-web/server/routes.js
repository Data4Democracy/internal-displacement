'use strict';

/**
 * Main application routes
 */

const path = require('path');
const bodyParser = require('body-parser');

module.exports = function (app) {

    app.use(bodyParser.json()); // for parsing application/json
    app.use(bodyParser.urlencoded({ extended: true })); // for parsing application/x-www-form-urlencoded

    // Insert routes below
    app.use('/api/test', require('./api/test'));
    app.use('/api/testDB', require('./api/sampleArticleRequest'));

    // All other routes should redirect to the index.html
    app.route('/')
        .get((req, res) => {
            res.sendFile(path.resolve(app.get('appPath') + '/index.html'));
        });

    app.use(function (req, res, next) {
        res.setHeader('Access-Control-Allow-Origin', '*');
        res.setHeader('Access-Control-Allow-Methods', 'GET, POST');
        res.setHeader('Access-Control-Allow-Headers', 'X-Requested-With,content-type, Authorization');
        next();
    });
};

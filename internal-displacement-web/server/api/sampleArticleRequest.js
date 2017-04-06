const db = require('./../pgDB');

module.exports = function (req, res) {
    db.any("select * from article limit 1", [true])
        .then(data => {
            console.log(data);
            //todo need to check if data needs JSON.stringify
            res.json(data);
        })
        .catch(error => {
            console.log(error)
            res.status(500).json({error: error, message: 'query error'});
        });
};
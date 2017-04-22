const db = require('./../pgDB');

module.exports = function (req, res) {
    db.any("select * from ( (select * from report_location LEFT JOIN location on report_location.location = location.id) t1 inner join (select id, quantity from report where quantity is not null) t2 on t1.report= t2.id) t3 where t3.latlong is not null", [true])
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

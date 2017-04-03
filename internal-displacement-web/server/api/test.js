const request = require('request');
module.exports = function (req, res) {
    console.log('trying ot get test data');
    const dummyMapUrl = 'https://jamesleondufour.carto.com/api/v2/sql?q=select%20count,%20long,%20lat,%20date%20from%20public.gdelt_refugee_2016';
    request.get(dummyMapUrl, (err, resp, body) =>{


        if (resp.statusCode == 200) {
            res.json(body);
        } else {
            res.status(404).json({error: 'not foubd'});
        }
    });

};


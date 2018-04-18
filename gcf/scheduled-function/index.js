const auth = require('./auth');
const settings = require('./settings.json');

exports.scheduled = function (req, res) {
    if (auth.authenticate(req, res, settings.credentials)) {
        console.info('Triggered function execution');
        res.status(200).end()
    }
};

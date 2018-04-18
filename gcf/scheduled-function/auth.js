const auth = require('basic-auth');
const compare = require('tsscmp');

// based on https://github.com/jshttp/basic-auth example

function check(name, pass, credentials) {
    let valid = true;

    valid = compare(name, credentials.username) && valid;
    valid = compare(pass, credentials.password) && valid;

    return valid
}

exports.authenticate = function (req, res, credentials) {
    let reqCredentials = auth(req);

    if (!reqCredentials || !check(reqCredentials.name, reqCredentials.pass, credentials)) {
        res.set('WWW-Authenticate', 'Basic realm="scheduled"').status(401).end();
        return false
    }
    return true
};

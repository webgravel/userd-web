var net = require('net');
var http = require('http');
var child_process = require('child_process');

var cache_timeout = 20 * 1000
var cache = {};

function get_addr_for(host, ok, error) {
    var cached = cache[host];
    if(cached) {
        if(Date.now() < cached.time + cache_timeout)
            return ok(cached)
    }
    var proc = child_process.spawn("sudo", ["gravel-web-gettarget", host]);
    var buff = '';
    proc.stdout.on('data', function(data) {
        buff += data;
    })
    proc.stderr.on('data', function(data) {
        console.log("[gettarget] " + data)
    })
    proc.on('close', function(code) {
        if(code == 0) {
            var split = buff.split(' ');
            var addr = {host: split[0], port: parseInt(split[1]),
                       time: Date.now()}
            cache[host] = addr
            ok(addr);
        } else {
            error();
        }
    })
}

function process_ip(ip) {
    if(/^::ffff:[^:]+$/.test(ip)) {
        // normalize ipv6 form of ipv4 address to ipv4 address
        ip = ip.slice(7);
    }
    return ip;
}

var server = http.createServer(function(req, res) {
    var host = req.headers.host
    get_addr_for(host, function(addr) {
        var remote_ip = req.connection.remoteAddress;
        console.log(remote_ip, req.method, host, req.url,
                   '->', addr.host, addr.port);
        var remote_addr = process_ip(req.connection.remoteAddress)
        req.headers['X-Real-Ip'] = req.headers['X-Forwarded-For'] = remote_addr;
        var proxy_request = http.request({
            hostname: addr.host,
            port: addr.port,
            path: req.url,
            method: req.method,
            headers: req.headers});
        req.pipe(proxy_request)
        proxy_request.on('response', function(proxy_response) {
            proxy_response.pipe(res);
            res.writeHead(proxy_response.statusCode, proxy_response.headers);
        })
        proxy_request.on('error', function(e) {
            console.log('problem with request: ' + e.message);
            res.statusCode = 510;
            res.end(e.message);
        });
    }, function() {
        res.statusCode = 502;
        res.end('no such host');
    })
});

server.listen(80, '::', null, function() {
    try {
        process.setgid('daemon');
        process.setuid('proxy');
    } catch (err) {
        console.log('setuid/setgid failed');
        process.exit(1);
    }
});

userd-web
-----------

SSL setup
=========

You need to have default certificate, even if you will use SNI.

```
# create self-signed one
openssl req -new -x509 -keyout key.pem -out cert.pem -days 3650 -nodes
```

Create `/gravel/system/ssl/options.json` file:

```
$ python
>>> import json
>>> print >> open('options.json', 'w'), json.dumps({'key': open('key.pem').read(), 'cert': open('cert.pem').read()})
```

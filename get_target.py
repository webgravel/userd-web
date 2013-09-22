#!/usr/bin/env python2.7
import sys
import json

sys.path.append('/gravel/pkg/gravel-common')
sys.path.append('/gravel/pkg/gravel-userd')
sys.path.append('/gravel/pkg/gravel-userd-web')

import users
import userns
import domains

domain = sys.argv[1]
try:
    domain = domains.Domain(domain, autocreate=False)
except KeyError:
    sys.exit(1)

owner = domain.data.owner
port = domain.data.port
forward = domain.data.forward

if not forward:
    forward = userns.get_ip(owner * 4 + 2) # host address
    users.User(owner).activate()
print json.dumps({
    'host': forward,
    'port': port,
    'key': domain.data.key,
    'cert': domain.data.cert,
})

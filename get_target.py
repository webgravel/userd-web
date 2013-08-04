#!/usr/bin/env python2.7
import sys

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

ip = userns.get_ip(owner * 4 + 2) # host address
users.User(owner).activate()

print ip, port

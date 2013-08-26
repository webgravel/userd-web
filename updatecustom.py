#!/usr/bin/env python2.7
# Updates mapping used by reverse proxy.

import sys

sys.path.append('/gravel/pkg/gravel-common')
sys.path.append('/gravel/pkg/gravel-userd')

import users
import domains
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('uid', type=int)
args = parser.parse_args()

user = users.User(args.uid)

# todo: remove old domains

for prop in user.data.custom.get('web', []):
    host = prop['host']
    port = int(prop['port'])
    forward = prop.get('forward')
    domain = domains.Domain(host)
    domain.data.port = port
    domain.data.owner = args.uid
    domain.data.forward = forward
    domain.save()

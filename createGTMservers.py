#!/usr/bin/python

# createGTMservers.py
# Author: Brandon Frelich
# Version 1.0
#
# Script to just load up a bunch of random generic servers.
#
# Todo--- maybe clean up after?

import argparse
import sys
import requests
import json
import getpass
import uuid

#Setup command line arguments using Python argparse
parser = argparse.ArgumentParser(description='create a bunch of gtm servers')
parser.add_argument('--bigip', '-b', help='IP or hostname of BIG-IP Management or Self IP', required=True)
parser.add_argument('--count', help='Number of partitions and policies to create', required=True)

args = parser.parse_args()

contentTypeJsonHeader = {'Content-Type': 'application/json'}

#adapted from https://devcentral.f5.com/articles/demystifying-icontrol-rest-6-token-based-authentication
def get_auth_token():
    payload = {}
    payload['username'] = "admin"
    payload['password'] = "admin"
    payload['loginProviderName'] = 'tmos'
    authurl = 'https://%s/mgmt/shared/authn/login' % args.bigip
    token = bip.post(authurl, headers=contentTypeJsonHeader, auth=(user, passwd), data=json.dumps(payload)).json()['token']['token']
    return token

url_base = ('https://%s/mgmt/tm' % (args.bigip))
# Just defaults in lab
user = "admin"
passwd = "admin"
bip = requests.session()
bip.verify = False
requests.packages.urllib3.disable_warnings()
authtoken = get_auth_token()
authheader = {'X-F5-Auth-Token': authtoken}
bip.headers.update(authheader)

# combine two Python Dicts (our auth token and the Content-type json header) in preparation for doing POSTs
postHeaders = authheader
postHeaders.update(contentTypeJsonHeader)

def createGTMserver(authtoken,bip,addy):
        url = 'https://'+args.bigip+'/mgmt/tm/gtm/server'
        headers = {
            'Content-Type': 'application/json',
            'X-F5-Auth-Token': authtoken
        }
        payload = {
                "name": str(uuid.uuid4()),
                "datacenter": "/Common/vlan253",
                "monitor": "/Common/gateway_icmp",
                "virtualServerDiscovery": "disabled",
                "product": "generic-load-balancer",
                "addresses": [
                    {
                    "name": addy,
                    "translation": "none"
                    }
                ],
                "virtual-servers":[
                    {
                        "name": str(uuid.uuid4()), 
                        "destination": addy+":443"
                    }
                ]
            }
        resp = requests.post(url,headers=headers, data=json.dumps(payload), verify=False)

for instance in range(1, int(args.count) + 1):

    if fourthOctet == 255:
        thirdOctet += 1
        fourthOctet = 1

    address = '10.0.%s.%s' % (thirdOctet, fourthOctet)
    fourthOctet += 1

    createGTMserver(authtoken,args.bigip,address)

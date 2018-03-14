#!/usr/bin/python3

# https://pymotw.com/2/argparse/

import argparse
import json
import http.client
#import urllib
from base64 import b64encode
import sys
from pprint import pprint

#disable ssl cert verfiy
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

parser = argparse.ArgumentParser(description='Example with long option names')

parser.add_argument('-n', '--noarg', action="store_true", default=False)
parser.add_argument('-w', '--witharg', action="store", dest="witharg")
parser.add_argument('-w2', '--witharg2', action="store", dest="witharg2", type=int)

#print(parser.parse_args([ '--noarg', '--witharg', 'val', '--witharg2=3' ]))
opt = parser.parse_args()
print(opt)



# get auth token
addr='10.154.164.129'

connection = http.client.HTTPSConnection(addr )

headers = {'Content-type': 'application/json'}

post_dict = {"username":"admin", "password":"admin", "loginProviderName":"tmos"}

post_json = json.dumps(post_dict)

connection.request('POST', '/mgmt/shared/authn/login', post_json, headers)

response = connection.getresponse()
#print(response.read().decode())

#print(type(response.read().decode()))
response_temp = response.read().decode()

response_dict = dict(json.loads(response_temp))


print(type(response_dict))

pprint(response_dict)


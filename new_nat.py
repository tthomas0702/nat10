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

### EXAMPLE PARSER ###
parser = argparse.ArgumentParser(description='Example with long option names')

parser.add_argument('-n', '--noarg', action="store_true", default=False)
parser.add_argument('-w', '--witharg', action="store", dest="witharg")
parser.add_argument('-w2', '--witharg2', action="store", dest="witharg2", type=int)

#####################


# real parser args
parser.add_argument('-l', '--list', action="store_true", default=False,
                    help='list currently deployed nats')
parser.add_argument('-d', '--debug', action="store_true", default=False,
                    help='enable debug')
parser.add_argument('-a', '--address', action="store", dest="address",
                    default='10.154.164.129', help='IP address of BIG-IP use as NAT machine')
parser.add_argument('-u', '--username', action="store", dest="username",
                    default='admin', help='username for auth to BIG-IP')
parser.add_argument('-p', '--password', action="store", dest="password",
                    default='admin', help='password for auth to BIG-IP')

opt = parser.parse_args()

if opt.debug == True:
    print(opt)

def get(address, url, auth_token):
    headers = {'Content-type': 'application/json', 'X-F5-Auth-Token' : auth_token}
    try:
        connection = http.client.HTTPSConnection(address)
        connection.request('GET', url, headers=headers)
    except ConnectionError:
        print('ConnectionError')
        sys.exit(0)
    except:
        raise
        sys.exit(0)
    r1 = connection.getresponse()
    data1 = r1.read()
    return data1.decode("utf-8")


def post(address, url, auth_token, post_data):
    headers = {'Content-type': 'application/json', 'X-F5-Auth-Token' : auth_token}
    post_json = json.dumps(post_data)
    try:
        connection = http.client.HTTPSConnection(address)
        connection.request('POST', url, post_json, headers)
    except ConnectionError:
        print('ConnectionError')
        sys.exit(0)
    except:
        raise
        sys.exit(0)
    r1 = connection.getresponse()
    data1 = r1.read()
    return data1.decode("utf-8")


def get_auth_token(username, password, address):
    headers = {'Content-type': 'application/json'}
    post_dict = {"username":username, "password":password, "loginProviderName":"tmos"}
    post_json = json.dumps(post_dict)
    try:
        connection = http.client.HTTPSConnection(opt.address)
        connection.request('POST', '/mgmt/shared/authn/login', post_json, headers=headers)
    except ConnectionError :
        print('ConnectionError')
        sys.exit(0)
    except:
        raise
        sys.exit(0)
    r1 = connection.getresponse()
    data1 = r1.read()
    data_dict = json.loads(data1.decode("utf-8"))
    token = data_dict['token']['token']
    return token

# get auth_token
auth_token = get_auth_token(opt.username, opt.password, opt.address)


# test get
#version_req = get(opt.address, '/mgmt/tm/sys/version', auth_token)
#print(version_req)
#print(type(version_req))

# list
if opt.list == True:
    print('*** List ***')
    # get list of iapps
    url = '/mgmt/tm/sys/application/service/?$select=name,variables'
    deployed_apps = get(opt.address, url, auth_token)
    deployed_dict = dict(json.loads(deployed_apps))
    bigip_dict = {}
    for i in deployed_dict['items']:
        bigip_dict.update({i['name']: 
            {'mgmt' : i['variables'][0]['value'], 
             'nat' : i['variables'][1]['value']}})
#pprint(bigip_dict)
for k in bigip_dict:
    print("{:10} {:20} {}".format( k, bigip_dict[k]['nat'] , bigip_dict[k]['mgmt']))





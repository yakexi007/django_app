#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys,os
import urllib, urllib2
import base64
import hmac
import hashlib
from hashlib import sha1
import time
import uuid
import json
from optparse import OptionParser
import ConfigParser
import traceback
import requests
import json
import redis
from multiprocessing.dummy import Pool

access_key_id = 'xxxxx';
access_key_secret = 'xxxxx';
cdn_server_address = 'https://xxxx'

def percent_encode(str):
    res = urllib.quote(str.decode(sys.stdin.encoding).encode('utf8'), '')
    res = res.replace('+', '%20')
    res = res.replace('*', '%2A')
    res = res.replace('%7E', '~')
    return res

def compute_signature(parameters, access_key_secret):
    sortedParameters = sorted(parameters.items(), key=lambda parameters: parameters[0])

    canonicalizedQueryString = ''
    for (k,v) in sortedParameters:
        canonicalizedQueryString += '&' + percent_encode(k) + '=' + percent_encode(v)

    stringToSign = 'GET&%2F&' + percent_encode(canonicalizedQueryString[1:])

    h = hmac.new(access_key_secret + "&", stringToSign, sha1)
    signature = base64.encodestring(h.digest()).strip()
    return signature

def compose_url(user_params):
    timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    parameters = { \
            'Format'        : 'JSON', \
            'Version'       : '2014-11-11', \
            'AccessKeyId'   : access_key_id, \
            'SignatureVersion'  : '1.0', \
            'SignatureMethod'   : 'HMAC-SHA1', \
            'SignatureNonce'    : str(uuid.uuid1()), \
            'TimeStamp'         : timestamp, \
    }

    for key in user_params.keys():
        parameters[key] = user_params[key]

    signature = compute_signature(parameters, access_key_secret)
    parameters['Signature'] = signature
    url = cdn_server_address + "/?" + urllib.urlencode(parameters)
    return url

def make_request(user_params, quiet=False):
    url = compose_url(user_params)
    #print url
    return url

def PushCdn(ObjectUrl):
    r = redis.Redis(host='127.0.0.1',port=6379)
    user_params = {'Action': 'PushObjectCache', 'ObjectPath': ObjectUrl, 'ObjectType': 'File'}
    rs = make_request(user_params)
    headers = {'content-type': 'application/json'}
    push_option = requests.get(rs,headers=headers)
    #print push_option.text
    result = push_option.json()
    try:
        if result['PushTaskId'] != '':
            r.set(ObjectUrl,'Success')
        else:
            r.set(ObjectUrl,'Failure')
    except Exception, e:
        r.set(ObjectUrl,'Failure')
    return result

def main(UrlList):
    rs = {}
    #create thread pool
    p = Pool(5)
    r = redis.Redis(host='127.0.0.1',port=6379)
    
    #start thread pool
    p.map(PushCdn,UrlList)
    p.close()
    p.join()

    for ObjectUrl in UrlList:
        rs[ObjectUrl] = r.get(ObjectUrl)
    return rs

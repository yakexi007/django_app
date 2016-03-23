#!/usr/bin/env python
# coding=utf-8

import requests
import json
import redis
import ConfigParser
import random
import sys 
import itertools
from multiprocessing.dummy import Pool,freeze_support
reload(sys)
sys.setdefaultencoding("utf-8")

# noinspection PyMethodMayBeStatic
class Redis:

    def __init__(self):
        self.__host = '127.0.0.1'
        self.__port = 6379
        self.r = redis.Redis(host=self.__host,port=self.__port)

    def set(self,key,data):
        self.r.set(key,data)
    
    def get(self,key):
        data = self.r.get(key)
        return data        

class saltAPI:

    def __init__(self):
        self.__user = 'saltapi'
        self.__password = 'shuqi_op@)!^'  # admin用户密码
        self.config = ConfigParser.ConfigParser()
        self.re = Redis()
        self.p = Pool(5)

    def salt_login(self, url):
        params = {'eauth': 'pam', 'username': self.__user, 'password': self.__password}
        url += '/login'
	r = requests.post(url, data=params,verify=False)
        content = r.json()
        try:
            token = content['return'][0]['token']
            return token
        except KeyError:
            raise KeyError

    def getHostlist(self):
        self.config.read('/home3/django_web/webapp/web.ini')
        hList = eval(self.config.get('check','hosts'))
        return hList

    def postRequest(self, url, params, token, prefix='/', ):
        url += prefix
        headers = {'X-Auth-Token': token,'Accept': 'application/json'}
	r = requests.post(url,headers=headers,data=params,verify=False)
        data = r.json()
        return data

    def saltDir(self, *info):
        url = 'https://10.32.38.219:8888'
        token = self.salt_login(url)
        params = {'client': 'local', 'fun': 'cmd.script', 'tgt': info[0][0], 'arg': ['salt://src/scripts/check_list_path1.py']}
        params['arg'].append(info[0][1])
        res = self.postRequest(url, params, token)
        res_data = res['return'][0][info[0][0]]['stdout']
        self.re.set(info[0][0]+'1',res_data)
        return 

    def getDir(self,info):
        Hlist = self.getHostlist()
        data = [(h,info) for h in Hlist]
        self.p.map(self.saltDir,data)
        self.p.close()
        self.p.join()
        demo = eval(self.re.get('sqdemo1' + '1'))
        del Hlist[0]
        get_data = {}
        for h in Hlist:
            result = eval(self.re.get(h + '1'))
            for key in result.keys():
                l = set(result[key]) - set(demo[key])
                if len(data) > 0:
                    result[key] = list(l)
            get_data[h] = result
        return get_data

    def saltMd5(self,*info):
        url = 'https://10.32.38.219:8888'
        token = self.salt_login(url)
        params = {'client': 'local', 'fun': 'cmd.script', 'tgt': info[0][0], 'arg': ['salt://src/scripts/check_md5_file.py']}
        params['arg'].append(info[0][1])
        res = self.postRequest(url, params, token)
        res_data = res['return'][0][info[0][0]]['stdout']
        self.re.set(info[0][0],res_data)
        return

    def getMd5(self,info):
        Hlist = self.getHostlist()
        data = [(h,info) for h in Hlist]
        self.p.map(self.saltMd5,data)
        self.p.close()
        self.p.join()
        demo = eval(self.re.get('sqdemo1'))
        del Hlist[0]
        get_data = {}
        for h in Hlist:
            result = eval(self.re.get(h))
            for k,v in result.items():
                if result[k] == 'free file':
                    result[k] = 'file not exit'
                elif result[k] == demo[k]:
                    result[k] = 'OK'
                else:
                    result[k] = 'Fail'
            get_data[h] = result
        return get_data 

if __name__ == '__main__':
    client = saltAPI()
    #params = {'client': 'local', 'fun': 'cmd.script', 'tgt': 'sqdemo1', 'arg': ['salt://src/scripts/check_list_path1.py',"/home/#/work/"]}
    #print client.saltCmd('/tmp/test.txt#/tmp/test1.txt')
    #print client.getMd5('/tmp/test.txt#/tmp/test1.txt#/tmp/test2#/tmp/test3#/tmp/test22#/tmp/test2123')
    print client.getDir('/work#/usr/local/')

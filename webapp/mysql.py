#!/usr/bin/env  python
#coding:utf-8

import datetime
from models import history_data

def mysql_insert(person,types,reason,path,result):
    dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    h = history_data(datetime=dt,person=person,types=types,\
        reason=reason,path=path,result=result)
    h.save()
    return 'ok'

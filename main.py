#!/usr/bin/env python
# -*- coding: utf-8 -*-

from config import account_name, account_key
from azure.storage import TableService, Entity
import time

#解决中文编码问题
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

#登陆
table_service = TableService(account_name=account_name, account_key=account_key)

#创建test
table_service.create_table('test');

moment = {
     'PartitionKey' : 'demo',
     'RowKey' : '3',
     'message' : 'hello windows world!',
     'time' : time.strftime('%a, %d %b %Y %H:%M:%S %Z', time.localtime())
}

#插入
try:
    table_service.insert_entity('test', moment)
except:
    pass

#查询
moments = table_service.query_entities('test', "PartitionKey eq 'demo'")
for moment in moments:
    print moment.time, moment.message


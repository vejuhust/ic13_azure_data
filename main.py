#!/usr/bin/env python
# -*- coding: utf-8 -*-

from config import account_name, account_key
from azure.storage import *
import time
import datetime
import re
import json

#解决中文编码问题
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


#类
class HealthDataAzure:
    #表名
    TABLE_USER = 'User'
    TABLE_TEMPERATURE = 'BodyTemperature'
    TABLE_HEARTBLOOD = 'HeartRateBloodPressure'
    TABLE_MESSAGE = 'Message'
    USER_PROFILE = 'Profile'
    USER_COUNT = 'DataCount'
    
    
    #初始化
    def __init__(self, name = account_name, key = account_key):
        #登陆
        self.table_service = TableService(account_name = name, account_key = key)
        #创建表格
        self.table_service.create_table(self.TABLE_USER)
        self.table_service.create_table(self.TABLE_TEMPERATURE)
        self.table_service.create_table(self.TABLE_HEARTBLOOD)
        self.table_service.create_table(self.TABLE_MESSAGE)

    
    #将Entity转化为dictionary
    def __entity_to_dict(self, entity):
        key_lists = dir(entity)
        result = {}
        pattern_attr = re.compile(u'^__.*__$')
        for key in key_lists:
            if pattern_attr.findall(key) == []:
                result[key] = getattr(entity, key)
        return result
    
    
    #查询所有表格
    def get_all_tables(self):
        result = []
        tables = self.table_service.query_tables()
        for table in tables:
            result.append(self.__entity_to_dict(table))
        return result
    

    #获取所有用户
    def get_all_users(self):
        result = []
        users = self.table_service.query_entities(self.TABLE_USER)
        for user in users:
            result.append(self.__entity_to_dict(user))
        return result


    #查询用户信息
    #用户存在返回Entity，用户不存在返回None
    def get_user(self, username):
        try:
            user = self.table_service.get_entity(self.TABLE_USER, username, self.USER_PROFILE)
        except:
            return None
        else:
            return self.__entity_to_dict(user)


    #添加用户
    #添加成功返回True，添加失败返返回False
    def add_user(self, username, password):
        if (self.get_user(username) == None):
            user = {
                'PartitionKey' : username,
                'RowKey' : self.USER_PROFILE,
                'Username' : username,
                'Password' : password,
                'Date' : datetime.datetime.today()
            }
            try:
                self.table_service.insert_entity(self.TABLE_USER, user)
            except:
                return False
            else:
                return True
        else:
            return False


    #删除用户及其存储标记
    #删除成功返回True，删除失败返回False
    def delete_user(self, username):
        try:
            self.table_service.delete_entity(self.TABLE_USER, username, self.USER_PROFILE)
        except:
            return False
        else:
            try:
                self.table_service.delete_entity(self.TABLE_USER, username, self.USER_COUNT)
            except:
                pass
            finally:
                return True


    #更新用户密码
    #更新成功返回True，更新失败返回False
    def update_user(self, username, password):
        if (self.get_user(username) == None):
            return False
        else:
            user = {
                'PartitionKey' : username,
                'RowKey' : self.USER_PROFILE,
                'Username' : username,
                'Password' : password,
                'Date' : datetime.datetime.today()
            }
            try:
                self.table_service.update_entity(self.TABLE_USER, username, self.USER_PROFILE, user)
            except:
                return False
            else:
                return True


#打印JSON格式输出
def print_json(description, item):
    print description, 
    try:
        print json.dumps(item, sort_keys=True, indent=4)
    except:
        print item



d = HealthDataAzure()

print_json(u'获取所有表格，四枚', d.get_all_tables()  )
print_json(u'获取所有用户，应当为空', d.get_all_users()   )
print_json(u'添加用户user1，成功', d.add_user('user1', 'password1')    )
print_json(u'重复添加用户user1，失败', d.add_user('user1', 'password1')    )
print_json(u'添加用户user2，成功', d.add_user('user2', 'password2')    )
print_json(u'获取未知用户USER1，失败', d.get_user('USER1') )
print_json(u'获取用户user2，成功', d.get_user('user2') )
print_json(u'获取所有用户，两枚', d.get_all_users()   )
print_json(u'删除用户user1，成功', d.delete_user('user1')  )
print_json(u'删除用户user2，成功', d.delete_user('user2')  )
print_json(u'获取所有用户，应当为空', d.get_all_users()   )
print_json(u'删除未知用户hello，失败', d.delete_user('hello')  )
print_json(u'添加用户user3，成功', d.add_user('user3', 'passwordXXX')  )
print_json(u'获取用户user3，成功', d.get_user('user3') )
print_json(u'更新用户user3，成功', d.update_user('user3', 'PASSWORD333')   )
print_json(u'获取用户user3，成功', d.get_user('user3') )
print_json(u'删除用户user3，成功', d.delete_user('user3')  )
print_json(u'更新未知用户user4，失败', d.update_user('user4', 'PASSWORDFour')  )
print_json(u'获取所有用户，应当为空', d.get_all_users()   )



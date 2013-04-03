#!/usr/bin/env python
# -*- coding: utf-8 -*-

from config import account_name, account_key
from azure.storage import *
import time
import datetime
import re


class HealthDataAzure:
    #表名
    TABLE_USER = 'User'
    TABLE_TEMPERATURE = 'BodyTemperature'
    TABLE_HEARTBLOOD = 'HeartRateBloodPressure'
    TABLE_MESSAGE = 'Message'
    DATA_TABLE_LIST = [TABLE_TEMPERATURE, TABLE_HEARTBLOOD, TABLE_MESSAGE]
    ALL_TABLE_LIST = DATA_TABLE_LIST + [TABLE_USER]
    
    USER_PROFILE = 'Profile'
    USER_COUNT = 'DataCount'
    
    
    #初始化
    def __init__(self, name = account_name, key = account_key):
        #登陆
        self.table_service = TableService(account_name = name, account_key = key)
        #创建表格
        for table_name in self.ALL_TABLE_LIST:
            self.table_service.create_table(table_name)


    def reset_all_tables(self):
        #删除旧表格
        for table_name in self.ALL_TABLE_LIST:
            self.table_service.delete_table(table_name)
        #创建表格
        for table_name in self.ALL_TABLE_LIST:
            self.table_service.create_table(table_name)
    
    
    #将Entity转化为dictionary
    def __entity_to_dict(self, entity):
        key_lists = dir(entity)
        result = {}
        pattern_attr = re.compile(u'^__.*__$')
        for key in key_lists:
            if (pattern_attr.findall(key) == []) and (key != 'etag'):
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


    #删除用户及其关联数据
    #删除成功返回True，删除失败返回False
    def delete_user(self, username):
        try:
            self.table_service.delete_entity(self.TABLE_USER, username, self.USER_PROFILE)
        except:
            return False
        else:
            self.__delete_data(username)
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



    #将缩略词转为对应表名
    def __abbr_to_name(self, abbr):
        for table_name in self.DATA_TABLE_LIST:
            if abbr.lower() in table_name.lower():
                return table_name
        return None


    #获取用户数据信息
    def get_data(self, username, table_abbr):
        #不存在的表返回空
        result = []
        table_name = self.__abbr_to_name(table_abbr)
        if table_name  == None:
            return result
        #获取已知表的前top个数据
        data = self.table_service.query_entities(table_name, filter = "PartitionKey eq '%s'" % username)
        for item in data:
            result.append(self.__entity_to_dict(item))
        return result


    #获取用户数据存量信息
    def __get_data_count(self, username, table_name):
        try:
            data = self.table_service.get_entity(self.TABLE_USER, username, self.USER_COUNT)
        except:
            return 0
        else:
            if hasattr(data, table_name):
                return getattr(data, table_name)
            else:
                return 0


    #设置用户数据存量信息
    def __set_data_count(self, username, table_name, count):
        try:
            #判断是否存在count的Entity
            data = self.table_service.get_entity(self.TABLE_USER, username, self.USER_COUNT)
        except:
            data = {
                'PartitionKey' : username,
                'RowKey' : self.USER_COUNT,
                'Username' : username,
                table_name : count
            }
            try:
                #添加新的count的Entity
                self.table_service.insert_entity(self.TABLE_USER, data)
            except:
                return False
            else:
                return True
        else:
            data = self.__entity_to_dict(data)
            data[table_name] = count
            try:
                #更新已有count的Entity中的Table计数
                self.table_service.update_entity(self.TABLE_USER, username, self.USER_COUNT, data)
            except:
                return False
            else:
                return True


    #存入用户数据信息
    def add_data(self, username, table_abbr, data):
        #不存在的表返回False
        table_name = self.__abbr_to_name(table_abbr)
        if table_name  == None:
            return False
        #判断用户是否存在
        if (self.get_user(username) == None):
            return False
        #获取此类数据已有数量
        count = self.__get_data_count(username, table_name) + 1
        #添加数据属性
        data['PartitionKey'] = username
        data['RowKey'] = "%.8d" % count
        data['Date'] = datetime.datetime.today()
        #将数据插入Table
        try:
            self.table_service.insert_entity(table_name, data)
        except:
            return False
        else:
            #更新数据数量
            self.__set_data_count(username, table_name, count)
            return True


    #删除用户相关数据
    def __delete_data(self, username):
        #按表遍历
        for table_name in self.DATA_TABLE_LIST:
            #查看此类数据已有数量
            count = self.__get_data_count(username, table_name) + 1
            for index in range(1, count):
                try:
                    self.table_service.delete_entity(table_name, username, "%.8d" % index)
                except:
                    pass
        return True



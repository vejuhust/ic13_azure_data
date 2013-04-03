#!/usr/bin/env python
# -*- coding: utf-8 -*-

from HealthDataAzure import HealthDataAzure
import json

#解决中文编码问题
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


#打印JSON格式输出
def print_json(description, item):
    print description,
    try:
        print json.dumps(item, sort_keys=True, indent=4)
    except:
        print item


#测试代码
if __name__ == '__main__':
    #测试标记，改为1则重建所有表
    RESET_ALL_TABLES = 0
    
    #创建实例
    d = HealthDataAzure()

    #是否重建所有表
    if RESET_ALL_TABLES > 0:
        print u"重建所有表"
        d.reset_all_tables()
        exit()

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
    print_json(u'添加用户userdata，成功', d.add_user('userdata', 'passworduserdata')    )
    print_json(u'获取用户体温数据，应当为空', d.get_data('userdata', 'temp')  )
    print_json(u'插入用户温度数据36.3', d.add_data('userdata', 'temp', {'Temperature':36.3})   )
    print_json(u'插入用户血压数据175:220:190', d.add_data('userdata', 'heart', {'DiastolicPressure' : 175, 'SystolicPressure':220, 'MeanPressure' : 190}))
    print_json(u'获取用户体温数据，一枚', d.get_data('userdata', 'temp')  )
    print_json(u'插入用户温度数据38.9', d.add_data('userdata', 'temp', {'Temperature':38.9})   )
    print_json(u'插入用户温度数据48.9', d.add_data('userdata', 'temp', {'Temperature':48.9})   )
    print_json(u'插入用户温度数据58.9', d.add_data('userdata', 'temp', {'Temperature':58.9})   )
    print_json(u'插入用户温度数据52.9', d.add_data('userdata', 'temp', {'Temperature':52.9})   )
    print_json(u'插入用户温度数据68.9', d.add_data('userdata', 'temp', {'Temperature':68.9})   )
    print_json(u'插入用户温度数据78.9', d.add_data('userdata', 'temp', {'Temperature':78.9})   )
    print_json(u'插入用户温度数据88.9', d.add_data('userdata', 'temp', {'Temperature':88.9})   )
    print_json(u'获取用户体温数据，八枚', d.get_data('userdata', 'temp')  )
    print_json(u'插入用户血压数据75:120:100', d.add_data('userdata', 'heart', {'DiastolicPressure' : 75, 'SystolicPressure':120, 'MeanPressure' : 100}))
    print_json(u'获取用户血压数据，二枚', d.get_data('userdata', 'heart')  )
    print_json(u'获取所有用户，一枚', d.get_all_users()   )
    print_json(u'删除用户userdata，成功', d.delete_user('userdata')  )
    print_json(u'获取所有用户，应当为空', d.get_all_users()   )



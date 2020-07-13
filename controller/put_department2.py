'''
用于向企业微信通讯录中推送部门下面的校聘和自聘
2020年7月8日
彭琦
'''

from flask import Flask, render_template, request, flash
import pymysql
import requests
import json

'''
1. 获取token
'''
# 企业id 测试 ： ww552faed1b6936ee5
# 企业id  ： wwf5e4ddf3ff53c831
corpid = 'wwf5e4ddf3ff53c831'

# 通讯录secret 测试 ： Ba1jA84KaQA50bza7AgJeMlll1Xtm0Z53GLuni4D9yc
# 通讯录secret ： Jgd52Xlh_vRzXxtryWE8Qy10I2zLyy9JMnK_niXcZL0
corpsecret = 'Jgd52Xlh_vRzXxtryWE8Qy10I2zLyy9JMnK_niXcZL0'

# 发送get请求,请求access_token
request_date = {'corpid': corpid, 'corpsecret': corpsecret}
response = requests.get('https://qyapi.weixin.qq.com/cgi-bin/gettoken', params=request_date)

response_dict = response.json()
access_token = response_dict['access_token']
# flash("获取的access_token为：")
print(access_token)
# 已经获取到toke了

'''
2. 获取部门数据
'''

# 连接mysql数据库
con = pymysql.connect(
    host="222.203.0.6",
    user="pig",
    password="2020@bali",
    database="qywx",
    charset="utf8")

# 获得游标(获得一个可以执行SQL语句的迭代器)
cursor = con.cursor()                              # 创建游标
cursor.execute("select * from department_wechat_teacher")  # 执行sql语句

# 将数据放入元组
row_list1=[]
row_list2=[]
for result in cursor:
    # result[1]:name  # result[2]: id  result[3]：parent_id
    # 部门 11  学院  12   附属单位  13
    xp =  result[2] * 100 + 1
    zp =  result[2] * 100 + 2
    row_dict1 = {"name": '校聘', "parentid": result[2], "id": xp}
    row_dict2 = {"name": '自聘', "parentid": result[2], "id": zp}

    row_list1.append(row_dict1)
    row_list2.append(row_dict2)

print(row_list1)
print(row_list2)


'''
3. 发送到企业微信
请求方式：POST（HTTPS）
请求地址：https://qyapi.weixin.qq.com/cgi-bin/department/create?access_token=ACCESS_TOKEN

请求包体：
{
   "name": "广州研发中心",   必须
   "name_en": "RDGZ",
   "parentid": 1,           必须
   "order": 1,
   "id": 2
}
'''

url = 'https://qyapi.weixin.qq.com/cgi-bin/department/create'
# headers = {'Content-Type': 'application/json'}
params = {'access_token': access_token}
for data in row_list1:
    response = requests.post(url, params=params, data=json.dumps(data))
    print(response.text)
for data in row_list2:
    response = requests.post(url, params=params, data=json.dumps(data))
    print(response.text)





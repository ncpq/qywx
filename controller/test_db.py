import pymysql
con = pymysql.connect(
    host="222.203.0.6",
    user="pig",
    password="2020@bali",
    database="qywx",
    charset="utf8")

# 获得游标(获得一个可以执行SQL语句的迭代器)
cursor = con.cursor()

# 定义SQL语句
# %s需要去掉引号，pymysql会自动加上
gxnu_id = '20130044'
social_id = '450325198801160316'
name = '彭琦'
sql = 'select wechatpart_id from gxnu_user where gxnu_id=%s and social_id=%s and name=%s'
# execute帮我们做字符串拼接 , 多个变量组使用executemany，可以使用元组列表
# result为0表示没有数据，为1表示有1条数据
result = cursor.execute(sql, [gxnu_id, social_id, name])

if result > 0:
    row = cursor.fetchall()
    print(row[0][0])
'''
用于向gxnu_user表中推送微信通讯录部门ID
2020年7月8日
彭琦
'''
import pymysql

# 连接mysql数据库
con = pymysql.connect(
    host="222.203.0.6",
    user="pig",
    password="2020@bali",
    database="qywx",
    charset="utf8")

# 获得游标(获得一个可以执行SQL语句的迭代器)
cursor = con.cursor()  # 创建游标
cursor.execute("select * from department")  # 执行sql语句

all_row1 = []
for result in cursor:
    row = [result[0], result[1], '']
    all_row1.append(row)

print(all_row1)

cursor.execute("select * from department_wechat_teacher")  # 执行sql语句
all_row2 = []
for result in cursor:
    row = [result[0], result[1], result[2]]
    all_row2.append(row)

print(all_row2)

# all_row2是带有企业微信部门编号的，要将all_row1里面的 2 替换到all_row2里
for it1 in all_row1:
    if it1[0] == 'z01' or 'z02' or 'z03':
        it1[2] = 999
    for it2 in all_row2:
        if it1[0] == it2[0]:
            it1[2] = it2[2]

for item in all_row1:
    sql = "update gxnu_user set wechatpart_id = '%d' Where department ='%s';" % (item[2], item[1])
    cursor.execute(sql)
    con.commit()

cursor.close()
con.close()






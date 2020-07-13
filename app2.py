from flask import Flask, render_template, request, flash
import pymysql
import requests

app = Flask(__name__, template_folder='templates')
app.secret_key='yanshan'




@app.route('/', methods=['GET', 'POST'])
def check():

    # 认证的用户请求url中带有code信息获取用户code
    code = request.args.get('code')
    flash(code)

    # 企业id 测试 ： ww552faed1b6936ee5
    # 企业id  ： wwf5e4ddf3ff53c831
    corpid = 'ww552faed1b6936ee5'

    # 通讯录secret 测试 ： Ba1jA84KaQA50bza7AgJeMlll1Xtm0Z53GLuni4D9yc
    # 通讯录secret ： Jgd52Xlh_vRzXxtryWE8Qy10I2zLyy9JMnK_niXcZL0
    corpsecret = 'Ba1jA84KaQA50bza7AgJeMlll1Xtm0Z53GLuni4D9yc'

    # 发送get请求,请求access_token
    request_date = {'corpid': corpid, 'corpsecret': corpsecret}
    response = requests.get('https://qyapi.weixin.qq.com/cgi-bin/gettoken', params=request_date)

    # 打印出服务器响应的header信息
    # print("打印出服务器响应的header信息:", response.headers)
    # 打印出服务器响应的状态码
    # print("打印出服务器响应的状态码:", response.status_code)
    # 打印出响应信息
    # print("打印出响应信息:", response.text)
    # print('打印出access_token：', response.text)
    # 以json格式打印出响应信息
    # print(response.json())
    response_dict = response.json()
    access_token = response_dict['access_token']
    flash("获取的access_token为：")
    flash(access_token)
    # print("打印出request", response.request)
    # print("打印出请求的cookie：", response.cookies)

    # 通过code获取userid链接格式
    # https://qyapi.weixin.qq.com/cgi-bin/user/getuserinfo?access_token=ACCESS_TOKEN&code=CODE

    # 使用requests构造http请求
    # 获取userid
    request_date = {'access_token': access_token, 'code': code}
    response = requests.get('https://qyapi.weixin.qq.com/cgi-bin/user/getuserinfo', params=request_date)

    # 1.判断请求方式
    if request.method == 'POST':

        # 2.获取请求参数
        gxnu_id = request.form.get('gxnu_id')
        name = request.form.get('name')
        social_id = request.form.get('social_id')

        if not all([gxnu_id, name, social_id]):
            print('参数不完整')
        else:
            # 连接mysql数据库
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
            sql = 'select * from gxnu_user where gxnu_id=%s and social_id=%s and name=%s'
            # execute帮我们做字符串拼接 , 多个变量组使用executemany，可以使用元组列表
            # result为0表示没有数据，为1表示有1条数据
            result = cursor.execute(sql, [gxnu_id, social_id, name])
            if result > 0:
                return 'sucess'
            cursor.close()
            con.close()

            # 查询成功返回微信

    return render_template('qywx_check.html')


if __name__ == '__main__':
    app.run(debug=True)

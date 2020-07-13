from flask import Flask, render_template, request, flash
import pymysql
import requests
import json

app = Flask(__name__, template_folder='templates')
app.secret_key='yanshan'


@app.route('/check/', methods=['GET', 'POST'])
def check():
    # 1.判断请求方式
    if request.method == 'POST':

        # 先获取用户的code
        code = request.args.get('code')
        # flash(code)
        # print(code)
        if (code==None):
            flash('请先关注广西师范大学企业微信')
            return render_template('qywx_check.html')

        # 2.获取请求参数
        gxnu_id = request.form.get('gxnu_id')
        name = request.form.get('name')
        social_id = request.form.get('social_id')

        if not all([gxnu_id, name, social_id]):
            flash('参数不完整')
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
            sql = 'select wechatpart_id from gxnu_user where gxnu_id=%s and social_id=%s and name=%s'
            # execute帮我们做字符串拼接 , 多个变量组使用executemany，可以使用元组列表
            # result为0表示没有数据，为1表示有1条数据
            result = cursor.execute(sql, [gxnu_id, social_id, name])
            if result > 0:

                row = cursor.fetchall()
                wechatpart_id = row[0][0]

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
                # flash(access_token)
                # 已经获取到toke了

                # 通过code获取userid链接格式
                # https://qyapi.weixin.qq.com/cgi-bin/user/getuserinfo?access_token=ACCESS_TOKEN&code=CODE
                request_date = {'access_token': access_token, 'code': code}
                response = requests.get('https://qyapi.weixin.qq.com/cgi-bin/user/getuserinfo', params=request_date)
                response_dict = response.json()
                # flash(response_dict)
                wxid = response_dict['UserId']
                # flash(wxid)

                # 获取了userid后让它加入企业
                # 请求方式：GET（HTTPS）
                # 请求地址：https://qyapi.weixin.qq.com/cgi-bin/user/authsucc?access_token=ACCESS_TOKEN&userid=USERID

                request_date = {'access_token': access_token, 'userid': wxid}
                response = requests.get('https://qyapi.weixin.qq.com/cgi-bin/user/authsucc', params=request_date)
                response_dict = response.json()
                flash(response_dict)
                errmsg = response_dict['errmsg']
                errcode = response_dict['errcode']
                if errmsg == 'ok':
                    flash(name)
                    flash('恭喜你成功加入广西师范大学企业微信！！')

                    # 更新成员信息
                    # 请求方式：POST（HTTPS）
                    # https://qyapi.weixin.qq.com/cgi-bin/user/update?access_token=ACCESS_TOKEN
                    # 请求包体
                    '''
                    {
                        "userid": "zhangsan",      原id
                        "new_userid": "zhangsan",  工号 
                        "name": "李四",             姓名
                        "department": [1]           部门列表
                    }
                    '''
                    url = 'https://qyapi.weixin.qq.com/cgi-bin/user/update'
                    de_list = []
                    de_list.append(wechatpart_id)
                    params = {'access_token': access_token}
                    data= {"userid": wxid, "new_userid": gxnu_id, "name": name,"department": de_list}
                    response = requests.post(url, params=params, data=json.dumps(data))
                    # flash(response.text)

                else:
                    flash('加入失败！错误代码为：')
                    flash(errcode)
                cursor.close()
                con.close()
                return render_template('qywx_check_sucess.html')
            else:
                flash('您的信息不对，请联系客服QQ：232162670')

    return render_template('qywx_check.html')

if __name__ == '__main__':
    app.run()

from flask import Flask, request, jsonify, make_response, send_file
from flask_cors import CORS
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, unset_jwt_cookies
from captcha.image import ImageCaptcha
from datetime import timedelta
import datetime
import requests
import json 
import csv
import os
import sys
from file import log_request, create_zip, log_download, create_zip_file, write_txt_files, fetch_data
import random
import wv_sql as sql
from wv_sql import Database
import email_post as ep



app = Flask(__name__)
CORS(app)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['JWT_SECRET_KEY'] = '8v94b6012q3rcnhcsejrfrt4'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=30000)
# auto_sign_scheduler = APScheduler()
# auto_sign_scheduler.init_app(app)

# 初始化 Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
# 初始化 Flask-JWT-Extended
jwt = JWTManager(app)

# 验证码字符集
CHARACTER_SET = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'


class User(UserMixin):
    def __init__(self, id):
        self.id = id


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


@app.route('/api/login', methods=['POST'])
def ct_login():
    username = request.form.get('username')
    password = request.form.get('password')

    if sql.authenticate_user(username, password):
        username_from_qq = sql.get_username_by_qq_number(username)
        if username_from_qq:
            username = username_from_qq
        user = User(username)
        login_user(user)

        # 使用用户名作为额外的密钥信息
        access_token = create_access_token(identity=username, additional_claims={'username': username})
        user_info = sql.get_user_info_by_username(username)
        # print(user_info)

        # print(type(user_info))
        sql.refersh_user_login_time(user_info['id'])
        sql.increment_login_times(user_info['id'])
        return jsonify({
            "login": True,
            "access_token": access_token,
            "user_info": user_info
        })
    else:
        return jsonify({'login': False})


@app.route('/api/checkLoginStatus')
@jwt_required()
def check_login_status():
    identity = get_jwt_identity()

    user_info = sql.get_user_info_by_username(identity)
    return jsonify({'logged_in': True,
                    'user_info': user_info
                    })


@jwt.expired_token_loader
def my_expired_token_callback(jwt_header, jwt_payload):
    """返回 flask Response 格式"""
    return jsonify({"logged_in": False,
                    "msg": "token 已过期"
                    })


@app.route('/api/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    qq = request.form.get('qq')
    captcha = request.form.get('captcha').lower()
    captcha_seed = request.form.get('captcha_seed')

    if (username == "" or password == "" or qq == ""):
        return jsonify({'message': '参数不完整',
                        'code': 400
                        })

    # 根据 seed 重新生成相同的验证码
    random.seed(captcha_seed)
    correct_captcha = ''.join(random.choice(CHARACTER_SET) for _ in range(4)).lower()

    if captcha != correct_captcha:
        return jsonify({'message': '验证码错误',
                        'code': 400
                        })

    # 创建用户对象
    user = sql.User(username, password, qq)
    register_msg = sql.register_user(user)
    if register_msg['msg'] == "注册成功":
        return jsonify({'message': '注册成功',
                        'code': 200
                        })
    else:
        return jsonify({'message': register_msg['msg'],
                        'code': 400
                        })


@app.route('/api/find', methods=['POST'])
def find():
    email = request.form.get('email')
    captcha = request.form.get('captcha').lower()
    captcha_seed = request.form.get('captcha_seed')

    if (email == ""):
        return jsonify({'message': '参数不完整',
                        'code': 400
                        })

    # 根据 seed 重新生成相同的验证码
    random.seed(captcha_seed)
    correct_captcha = ''.join(random.choice(CHARACTER_SET) for _ in range(4)).lower()

    if captcha != correct_captcha:
        return jsonify({'message': '验证码错误',
                        'code': 400
                        })

    username = sql.get_username_by_qq_or_email(email)
    if username:
        ep.send_find_email(email)
        return jsonify({'message': '已发送重置链接至邮箱',
                        'code': 200
                        })
    else:
        return jsonify({'message': '找不到此用户',
                        'code': 400
                        })


@app.route('/api/resetPassword', methods=['POST'])
def resetPassword():
    password = request.form.get('password')
    reset_token = request.form.get('reset_token')

    if (password == "" or reset_token == ""):
        return jsonify({'message': '参数不完整',
                        'code': 400
                        })

    email = sql.check_reset_token_validity(reset_token).get('data').get('email')
    username = sql.get_username_by_qq_or_email(email)
    resp = sql.reset_password(username, password)

    if resp['success'] == False:
        return jsonify({'message': resp['msg'],
                        'code': 400
                        })
    else:
        sql.use_reset_token(reset_token)
        return jsonify({'message': resp['msg'],
                        'code': 200
                        })


@app.route('/api/checkResetToken', methods=['GET', 'POST'])
def checkResetToken():
    reset_token = request.args.get('reset_token')

    if (reset_token == ""):
        return jsonify({'message': '参数不完整',
                        'code': 400
                        })

    resp = sql.check_reset_token_validity(reset_token)
    if resp['success'] == False:
        return jsonify({'message': resp['msg'],
                        'code': 400
                        })
    else:
        return jsonify({'message': resp['msg'],
                        'code': 200
                        })




@app.route('/api/hello', methods=['GET'])
def hello():
    return jsonify({'message': 'Hello, World!'})


@app.route('/api/captcha', methods=['GET'])
def captcha():
    # 获取 URL 参数中的 seed 或者生成新的随机种子
    seed = request.args.get('seed')
    if seed is None:
        seed = str(random.randint(1000, 9999))

    try:
        # 设置随机种子
        random.seed(seed)

        # 生成4位验证码
        captcha_text = ''.join(random.choice(CHARACTER_SET) for _ in range(4))
        # print(captcha_text)

        # 创建验证码图片
        image = ImageCaptcha()
        data = image.generate(captcha_text)

        # 返回验证码图片
        response = make_response(data.read())
        response.headers['Content-Type'] = 'image/png'
        return response
    except Exception as e:
        return str(e)


@app.route('/api/check_captcha', methods=['POST'])
def check_captcha():
    try:
        # 从表单中获取用户输入的验证码和 seed
        user_captcha = request.form.get('captcha').lower()
        seed = request.form.get('seed')

        # 根据 seed 重新生成相同的验证码
        random.seed(seed)
        correct_captcha = ''.join(random.choice(CHARACTER_SET) for _ in range(4)).lower()

        # 校验验证码是否正确
        if user_captcha == correct_captcha:
            return jsonify({'message': '验证码正确',
                            'code': 200
                            })
        else:
            return jsonify({'message': '验证码错误',
                            'code': 400
                            })
    except Exception as e:
        return jsonify({'message': '验证码错误',
                        'code': 400
                        })


@app.route('/api/weather/checkLocation', methods=['GET'])
def check_location():
    location = request.args.get('location')

    args = {
        'location': location,
        'key': '22da55be85c846dc8a0b57f6ea985808'
    }

    location_id = requests.get('https://geoapi.qweather.com/v2/city/lookup', params=args).json()
    # print(location_id)
    if location_id['code'] == '200':
        location_id = location_id.get('location')[0].get('id')
        return jsonify({'message': '位置正确',
                        'code': 200,
                        'location_id': location_id
                        })

    return jsonify({'message': '位置错误',
                    'code': 400
                    })


@app.route('/api/weather/now', methods=['GET'])
def get_weather_now():
    location = request.args.get('location')

    args = {
        'location': location,
        'key': '22da55be85c846dc8a0b57f6ea985808'
    }

    weather_now = requests.get('https://devapi.qweather.com/v7/weather/now', params=args).json()
    # print(weather_now)

    if weather_now['code'] == '200':
        return jsonify({'message': '天气获取成功',
                        'code': 200,
                        'data': weather_now.get('now')
                        })

    return jsonify({'message': '天气获取失败',
                    'code': 400
    })


@app.route('/api/weather/24h', methods=['GET'])
def get_weather_hours():
    location = request.args.get('location')
    
    args = {
        'location': location,
        'key': '22da55be85c846dc8a0b57f6ea985808'
    }

    weather_now = requests.get(f'https://devapi.qweather.com/v7/weather/24h', params=args).json()
    # print(weather_now)
    
    if weather_now['code'] == '200':
        return jsonify({'message': '天气获取成功',
                        'code': 200,
                        'data': weather_now.get('hourly')
                        })
    
    return jsonify({'message': '天气获取失败',
                    'code': 400
    })


@app.route('/api/weather/nationwide', methods=['GET'])
def get_weather_nationwide():
    timestamp = datetime.datetime.now().timestamp() * 1000

    args = {
        't': timestamp,
    }

    weather_now = requests.get('https://weather.cma.cn/api/map/weather/1', params=args).json()

    # print(weather_now)
    if weather_now.get('code') == 0:
        return jsonify({'message': '天气获取成功',
                        'code': 200,
                        'data': weather_now.get('data')
                        })
    
    return jsonify({'message': '天气获取失败',
                    'code': 400
                    })

# @app.route('/api/download', methods=['POST'])
# def download_files():
#     print(request.form)
    # zip_name = request.form.get('zip_name')
    # start_date = request.form.get('start_date')
    # end_date = request.form.get('end_date')
    # note = request.form.get('note')
    #
    #
    # if not zip_name or not start_date or not end_date or not note:
    #     return jsonify({"error": "zip_name, start_date, end_date, and note are required"}), 400
    #
    # try:
    #     # 创建压缩包并记录请求
    #     zip_filename = create_zip(start_date, end_date, zip_name)
    #     log_request(zip_name, start_date, end_date, note)
    #
    #     # 发送压缩包文件给前端
    #     return send_file(zip_filename, as_attachment=True)
    # except Exception as e:
    #     print(e)
    #     return jsonify({"error": str(e)}), 500

@app.route('/api/weather/cityTemperatureRank', methods=['GET'])
def get_city_list_by_temperature():
    result = sql.get_city_list_by_temperature()
    return jsonify({'message': '查询成功',
                    'code': 200,
                    'data': result
                    })

@app.route('/api/download', methods=['POST'])
def download_files():
    data = request.form
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    zip_name = data.get('zip_name')
    note = data.get('note')
    options = data.get('options')
    options = json.loads(options)

    # if not start_date or not end_date or not zip_name or not options:
    #     return jsonify({'error': 'Missing required parameters'}), 400
    #
    db = Database()
    raw_data,fields = fetch_data(db, start_date, end_date, options)

    if not raw_data:
        return jsonify({'error': 'No data found for the given date range'}), 404

    file_names = write_txt_files(raw_data,fields)
    zip_buffer = create_zip_file(file_names, zip_name)
    # 将下载记录写入数据库
    log_download(db, zip_name, start_date, end_date, note, options)
    return send_file(
        zip_buffer,
        mimetype='application/zip',
        as_attachment=True,
        download_name=f"{zip_name}.zip"
    )


@app.route('/api/logs', methods=['GET'])
def get_logs():
    db = Database()
    connection = db.connect()
    cursor = connection.cursor()

    query = 'SELECT * FROM download_log'
    cursor.execute(query)
    logs = cursor.fetchall()

    cursor.close()
    connection.close()
    return jsonify(logs)

@app.route('/api/weather/newsList', methods=['GET'])
def get_news_list_by_page():
    page_number_str = request.args.get('pageNumber', '0')
    page_size_str = request.args.get('pageSize', '10')
    news_type = request.args.get('newsType')
    try:
        page_number = int(page_number_str)
        page_size = int(page_size_str)
        page_list = sql.get_news_list_by_page(page_number, page_size, news_type)
        count = sql.get_news_count(news_type)
        return jsonify({'message': '查询成功',
                        'code': 200,
                        'data': {
                            'page_list': page_list,
                            'total': count
                        }
                        })
    except ValueError:
        return jsonify({'error': '非法的入参'}), 400


@app.route('/api/weather/news', methods=['GET'])
def get_news_by_id():
    idStr = request.args.get('id', '0')
    try:
        id = int(idStr)
        result = sql.get_news(id)
        return jsonify({'message': '查询成功',
                        'code': 200,
                        'data': result
                        })
    except ValueError:
        return jsonify({'error': '非法的入参'}), 400

@app.route('/api/delete_log/<int:log_id>', methods=['DELETE'])
def delete_download_log(log_id):
    db = Database()
    connection = db.connect()
    cursor = connection.cursor()

    # 查询要删除的日志记录是否存在
    query = 'SELECT * FROM download_log WHERE id = %s'
    cursor.execute(query, (log_id,))
    log = cursor.fetchone()
    if not log:
        cursor.close()
        connection.close()
        return jsonify({'error': 'Log not found'}), 404

    # 执行删除操作
    delete_query = 'DELETE FROM download_log WHERE id = %s'
    cursor.execute(delete_query, (log_id,))
    connection.commit()

    cursor.close()
    connection.close()
    return jsonify({'message': 'Log deleted successfully'})


if __name__ == '__main__':

    app.run(debug=False, port=9001, threaded=True)
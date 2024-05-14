import pymysql.cursors
from datetime import datetime
import hashlib

class Database:
    def __init__(self):
        self.host = '124.70.222.169'
        self.user = 'wv_v2'
        self.password = 'LCACcrtY7jY2ZJNh'
        self.db = 'wv_v2'

    def connect(self):
        return pymysql.connect(host=self.host,
                                user=self.user,
                                password=self.password,
                                db=self.db,
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor)

class User:
    def __init__(self, username, password, qq):
        self.username = username
        self.password = password
        self.qq = qq

class ActivityInfo:
    def __init__(self, ektId=None, ActivityName=None, ActivityTypeText=None, ActivityAddressAreaStr=None, ActivityAddress=None, ActivityTime=None, ActScore=None, ActivityIntroduction=None, YearTerm=None, ApplyOrgName=None, ActivityLevelText=None, ModuleCodeText=None, SponsorNames=None, OrganizerNames=None, ActivityQDDate=None, IsNeedSignInText=None, IsNeedSignOutText=None, ActivityQTDate=None, IsLimitStuNumText=None, LimitStuNumber=None, IsSignExamText=None, IsHandInHomeWorkText=None, GradeLimit=None, SexStr=None, CollegeLimitStr=None, SignWayText=None, CoverSock=None, longitude=None, latitude=None, InsertTime=None):
        self.ektId = ektId
        self.ActivityName = ActivityName
        self.ActivityTypeText = ActivityTypeText
        self.ActivityAddressAreaStr = ActivityAddressAreaStr
        self.ActivityAddress = ActivityAddress
        self.ActivityTime = ActivityTime
        self.ActScore = ActScore
        self.ActivityIntroduction = ActivityIntroduction
        self.YearTerm = YearTerm
        self.ApplyOrgName = ApplyOrgName
        self.ActivityLevelText = ActivityLevelText
        self.ModuleCodeText = ModuleCodeText
        self.SponsorNames = SponsorNames
        self.OrganizerNames = OrganizerNames
        self.ActivityQDDate = ActivityQDDate
        self.IsNeedSignInText = IsNeedSignInText
        self.IsNeedSignOutText = IsNeedSignOutText
        self.ActivityQTDate = ActivityQTDate
        self.IsLimitStuNumText = IsLimitStuNumText
        self.LimitStuNumber = LimitStuNumber
        self.IsSignExamText = IsSignExamText
        self.IsHandInHomeWorkText = IsHandInHomeWorkText
        self.GradeLimit = GradeLimit
        self.SexStr = SexStr
        self.CollegeLimitStr = CollegeLimitStr
        self.SignWayText = SignWayText
        self.CoverSock = CoverSock
        self.longitude = longitude
        self.latitude = latitude
        self.InsertTime = InsertTime or datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def hash_password(password):
    # 使用SHA-256哈希函数对密码进行加密
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return hashed_password

# 检查用户名是否已存在
def check_username_exists(cursor, username):
    # 查询数据库，检查用户名是否已经存在
    sql = "SELECT * FROM user WHERE username = %s"
    cursor.execute(sql, (username,))
    return cursor.fetchone() is not None

# 注册用户
def register_user(user):
    database = Database()
    # 连接数据库
    with database.connect() as connection:
        try:
            with connection.cursor() as cursor:
                # 检查用户名是否已存在
                if check_username_exists(cursor, user.username):
                    # print("用户名已存在")
                    return {"msg": "用户名已存在"}
                
                # 对密码进行哈希加密
                hashed_password = hash_password(user.password)
                
                # 创建一个新用户记录
                register_time = datetime.now()
                sql = "INSERT INTO user (username, qq, pwd, register_time, is_vip, login_times, request_times) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (user.username, user.qq, hashed_password, register_time, 0, 0, 0))
        
            # 提交更改
            connection.commit()
            # print("注册成功！")
            return {"msg": "注册成功"}

        except pymysql.Error as e:
            print(f"注册失败: {e}")
            return {"msg": "注册失败"}

# 注册用户
def register_user(user):
    database = Database()
    # 连接数据库
    with database.connect() as connection:
        try:
            with connection.cursor() as cursor:
                # 检查用户名是否已存在
                if check_username_exists(cursor, user.username):
                    # print("用户名已存在")
                    return {"msg": "用户名已存在"}
                
                # 对密码进行哈希加密
                hashed_password = hash_password(user.password)
                
                # 创建一个新用户记录
                register_time = datetime.now()
                sql = "INSERT INTO 3ct_user (username, qq, pwd, register_time, is_vip, login_times, request_times) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (user.username, user.qq, hashed_password, register_time, 0, 0, 0))
        
            # 提交更改
            connection.commit()
            # print("注册成功！")
            return {"msg": "注册成功"}

        except pymysql.Error as e:
            print(f"注册失败: {e}")
            return {"msg": "注册失败"}

# 校验用户登录
def authenticate_user(username_or_qq, password):
    # 连接数据库
    database = Database()
    with database.connect() as connection:
        try:
            with connection.cursor() as cursor:
                # 确定是否是 QQ 邮箱
                if username_or_qq.endswith('@qq.com'):
                    # 去掉 "@qq.com" 部分，得到 QQ 号
                    qq_number = username_or_qq.replace('@qq.com', '')
                else:
                    # 否则使用提供的凭据作为 QQ 号
                    qq_number = username_or_qq
                
                # 查询数据库，检查用户名、QQ号或 QQ 邮箱是否存在
                sql = """
                    SELECT * FROM user 
                    WHERE username = %s OR qq = %s
                """
                # 执行查询，查询 QQ号两次，一个直接查询，一个通过 email 查询
                cursor.execute(sql, (username_or_qq, qq_number))
                
                user = cursor.fetchone()
                
                if not user:
                    # 如果没有找到用户，返回 False
                    print("用户不存在")
                    return False
                
                # 对输入的密码进行哈希加密，并与数据库中的加密密码进行比对
                hashed_input_password = hash_password(password)
                
                if user['pwd'] == hashed_input_password:
                    # 如果密码匹配，返回 True
                    # print("登录成功！")
                    return True
                else:
                    # 如果密码不匹配，返回 False
                    print("密码错误")
                    return False

        except pymysql.Error as e:
            print(f"认证失败: {e}")
            return False

def change_password(username, old_password, new_password):
    database = Database()
    # 连接数据库
    with database.connect() as connection:
        try:
            with connection.cursor() as cursor:
                # 查询数据库，检查用户名是否存在
                sql = "SELECT * FROM user WHERE username = %s"
                cursor.execute(sql, (username,))
                user = cursor.fetchone()
                
                if not user:
                    # 如果没有找到用户，返回 False
                    print("用户不存在")
                    return {
                        "success": False,
                        "msg": "用户不存在"
                    }
                
                # 对输入的密码进行哈希加密，并与数据库中的加密密码进行比对
                hashed_old_password = hash_password(old_password)
                
                if user['pwd'] == hashed_old_password:
                    # 如果密码匹配，更新密码
                    hashed_new_password = hash_password(new_password)
                    sql_update = "UPDATE user SET pwd = %s WHERE username = %s"
                    cursor.execute(sql_update, (hashed_new_password, username))
                    
                    # 提交更改
                    connection.commit()
                    # print("密码修改成功！")
                    return {
                        "success": True,
                        "msg": "密码修改成功"
                    }
                else:
                    # 如果密码不匹配，返回 False
                    print("旧密码错误")
                    return {
                        "success": False,
                        "msg": "旧密码错误"
                    }
                
        except pymysql.Error as e:
            print(f"密码修改失败: {e}")
            return {
                "success": False,
                "msg": "密码修改失败"
            }

def reset_password(username, new_password):
    database = Database()
    # 连接数据库
    with database.connect() as connection:
        try:
            with connection.cursor() as cursor:
                # 查询数据库，检查用户名是否存在
                sql = "SELECT * FROM user WHERE username = %s"
                cursor.execute(sql, (username,))
                user = cursor.fetchone()
                
                if not user:
                    # 如果没有找到用户，返回 False
                    print("用户不存在")
                    return {
                        "success": False,
                        "msg": "用户不存在"
                    }
                
                # 对输入的密码进行哈希加密，并与数据库中的加密密码进行比对
                hashed_new_password = hash_password(new_password)
                
                sql_update = "UPDATE user SET pwd = %s WHERE username = %s"
                cursor.execute(sql_update, (hashed_new_password, username))
                
                # 提交更改
                connection.commit()
                # print("密码重置成功！")
                return {
                    "success": True,
                    "msg": "密码重置成功"
                }
                
        except pymysql.Error as e:
            print(f"密码重置失败: {e}")
            return {
                "success": False,
                "msg": "密码重置失败"
            }

def get_username_by_qq_number(qq_number):
    try:
        # 连接数据库
        database = Database()
        with database.connect() as connection:
            with connection.cursor() as cursor:
                # 查询给定 QQ 号对应的用户名
                
                # 确定是否是 QQ 邮箱
                if qq_number.endswith('@qq.com'):
                    # 去掉 "@qq.com" 部分，得到 QQ 号
                    qq_number = qq_number.replace('@qq.com', '')
                else:
                    # 否则使用提供的凭据作为 QQ 号
                    qq_number = qq_number
                    
                sql = "SELECT username FROM user WHERE qq = %s"
                cursor.execute(sql, (qq_number,))
                
                # 获取查询结果
                user = cursor.fetchone()
                
                if user:
                    # 返回用户名
                    return user["username"]
                else:
                    # 如果未找到记录，则返回 None
                    return None

    except Exception as e:
        print(f"查询用户名失败: {e}")
        return None

# 获取用户信息（包含绑定平台信息）
def get_user_info_by_username(username):
    database = Database()
    # 连接数据库
    with database.connect() as connection:
        try:
            with connection.cursor() as cursor:
                # 查询用户信息
                sql_user = "SELECT id, username, qq, is_vip, is_tester, login_times, request_times FROM user WHERE username = %s"
                cursor.execute(sql_user, (username,))
                user = cursor.fetchone()
                if user:
                    # 构建JSON响应
                    user_info = {
                        "id": user["id"],
                        "username": user["username"],
                        "qq": user["qq"],
                        "is_vip": user["is_vip"],
                        "is_tester": user["is_tester"],
                        "login_times": user["login_times"],
                        "request_times": user["request_times"]
                    }
                    return user_info
                else:
                    return {"error": "用户不存在"}

        except pymysql.Error as e:
            print(f"获取用户信息失败: {e}")
            return {"error": "获取用户信息失败"}



def add_online_user(user_id):
    database = Database()
    login_time = datetime.now()
    # 连接数据库
    with database.connect() as connection:
        try:
            with connection.cursor() as cursor:
                # 检查用户是否存在于用户表中
                sql_check_user = "SELECT * FROM user WHERE id = %s"
                cursor.execute(sql_check_user, (user_id,))
                user = cursor.fetchone()
                if user:
                    # 用户存在，可以添加到在线用户表中
                    sql_add_online_user = "INSERT INTO 3ct_online_user (user_id, login_time) VALUES (%s, %s)"
                    cursor.execute(sql_add_online_user, (user_id, login_time))
                    connection.commit()
                    # print("添加在线用户成功！")
                else:
                    print("用户不存在，无法添加到在线用户表中")

        except pymysql.Error as e:
            print(f"添加在线用户失败: {e}")

# 增加用户登录次数
def increment_login_times(user_id):
    database = Database()
    # 连接数据库
    with database.connect() as connection:
        try:
            with connection.cursor() as cursor:
                # 增加用户登录次数
                sql = "UPDATE user SET login_times = login_times + 1 WHERE id = %s"
                cursor.execute(sql, (user_id,))
                
                # 提交更改
                connection.commit()
                # print("登录次数+1成功！")
                
        except pymysql.Error as e:
            print(f"增加登录次数失败: {e}")

# 增加用户请求次数
def increment_request_times(user_id):
    database = Database()
    # 连接数据库
    with database.connect() as connection:
        try:
            with connection.cursor() as cursor:
                # 增加用户请求次数
                sql = "UPDATE user SET request_times = request_times + 1 WHERE id = %s"
                cursor.execute(sql, (user_id,))
                
                # 提交更改
                connection.commit()
                # print("请求次数+1成功！")
                
        except pymysql.Error as e:
            print(f"增加请求次数失败: {e}")



def get_username_by_qq_or_email(qq_or_email):
    # 连接数据库
    database = Database()
    with database.connect() as connection:
        try:
            with connection.cursor() as cursor:
                # 查询用户名

                # 确定是否是 QQ 邮箱
                if qq_or_email.endswith('@qq.com'):
                    # 去掉 "@qq.com" 部分，得到 QQ 号
                    qq_number = qq_or_email.replace('@qq.com', '')
                else:
                    # 否则使用提供的凭据作为 QQ 号
                    qq_number = qq_or_email
                    
                sql_get_username = "SELECT username FROM user WHERE qq = %s"
                cursor.execute(sql_get_username, (qq_number,))
                
                username = cursor.fetchone()
                
                if username:
                    return username['username']
                else:
                    return None
                
        except Exception as e:
            print(f"查询用户名失败: {e}")
            return None
        

def save_token_to_db(email, token, expiration_time):
    # 连接数据库
    database = Database()
    with database.connect() as connection:
        try:
            with connection.cursor() as cursor:
                # 插入令牌、电子邮件和过期时间到 password_reset_tokens 表
                sql_insert_token = """
                    INSERT INTO password_reset_tokens (token, email, expiration_time, is_used)
                    VALUES (%s, %s, %s, FALSE)
                """
                cursor.execute(sql_insert_token, (token, email, expiration_time))
                
                # 提交事务
                connection.commit()
                
                print("令牌已成功保存到数据库")
                return {
                    'success': True,
                    'msg': '令牌已成功保存到数据库'
                }

        except pymysql.Error as e:
            print(f"保存令牌到数据库失败: {e}")
            return {
                'success': False,
                'msg': f'保存令牌到数据库失败: {str(e)}'
            }
        
def check_reset_token_validity(token):
    # 连接数据库
    database = Database()
    with database.connect() as connection:
        try:
            with connection.cursor() as cursor:
                # 查询令牌在 password_reset_tokens 表中
                sql_check_token = """
                    SELECT *
                    FROM password_reset_tokens
                    WHERE token = %s
                """
                cursor.execute(sql_check_token, (token,))
                
                token_data = cursor.fetchone()
                
                if not token_data:
                    # 如果找不到令牌，返回无效结果
                    return {
                        'success': False,
                        'msg': '无效的令牌'
                    }
                
                # 获取当前时间
                current_time = datetime.now()
                
                # 验证令牌是否过期
                expiration_time = token_data['expiration_time']
                if current_time > expiration_time:
                    # 令牌过期
                    return {
                        'success': False,
                        'msg': '令牌已过期'
                    }
                
                # 验证令牌是否已使用
                is_used = token_data['is_used']
                if is_used:
                    # 令牌已被使用
                    return {
                        'success': False,
                        'msg': '令牌已被使用'
                    }
                
                # 令牌有效
                return {
                    'success': True,
                    'msg': '令牌有效',
                    'data': token_data  # 返回令牌的详细信息
                }

        except Exception as e:
            print(f"检查令牌有效性失败: {e}")
            return {
                'success': False,
                'msg': f'检查令牌有效性失败: {str(e)}'
            }

def use_reset_token(token):
    # 连接数据库
    database = Database()
    with database.connect() as connection:
        try:
            with connection.cursor() as cursor:
                # 更新令牌状态为已使用
                sql_update_token = """
                    UPDATE password_reset_tokens
                    SET is_used = TRUE
                    WHERE token = %s
                    """
                cursor.execute(sql_update_token, (token,))
                
                # 提交事务
                connection.commit()
                
                return {
                    'success': True,
                    'msg': '令牌已成功标记为已使用'
                }
            
        except Exception as e:
            print(f"标记令牌为已使用失败: {e}")
            return {
                'success': False,
                'msg': f'标记令牌为已使用失败: {str(e)}'
            }


# 使用示例
if __name__ == "__main__":

    # # 创建用户对象
    # user = User(username='test2', password='123456', qq="12345")

    # # 注册用户
    # register_user(user)

    # 输入用户名和密码
    username = ''
    password = ''

    # 认证用户
    print(authenticate_user(username, password))


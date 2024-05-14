import wv_sql as sql
import uuid
from datetime import datetime, timedelta


BASE_URL = 'https://wv.2ndtool.top'

def generate_reset_link(user_email):
    # 生成唯一随机的令牌
    reset_token = str(uuid.uuid4())
    
    # 使用当前时间和有效期计算过期时间（15 分钟后）
    expiration_time = datetime.now() + timedelta(minutes=15)
    
    # 将令牌和过期时间存储到数据库中
    sql.save_token_to_db(user_email, reset_token, expiration_time)
    
    # 生成重置链接
    reset_link = f"{BASE_URL}/reset?token={reset_token}"
    
    return reset_link

# 示例使用
if __name__ == '__main__':
    user_email = '2050791391@qq.com'
    reset_link = generate_reset_link(user_email)
    print(f"Password reset link: {reset_link}")


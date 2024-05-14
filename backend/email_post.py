import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
import wv_func as func

# 配置日志记录
logging.basicConfig(level=logging.INFO)

# 邮箱服务器地址
MAIL_HOST = 'smtp.163.com'
# 用户名
MAIL_USER = 'alore_3ct'
# 授权码
MAIL_PASS = 'KQDZOKUAJSSBIOOW'
# 发件人邮箱地址
SENDER_EMAIL = 'alore_3ct@163.com'

# 找回账号的 HTML 内容模板
FIND_HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>【Weather Vista】账号找回</title>
</head>
<body style="font-family: Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 20px;">
    <div style="background-color: #ffffff; padding: 20px; border-radius: 8px; max-width: 600px; margin: 0 auto;">
        <h1 style="font-size: 24px; color: #333333;">找回账号</h1>
        <p style="font-size: 16px; line-height: 1.5; color: #666666;">你好，</p>
        <p style="font-size: 16px; line-height: 1.5; color: #666666;">
            我们收到了一个找回账号的请求。如果这是你本人操作，请点击下面的链接重置你的密码：
        </p>
        <p><a href="{reset_link}" style="display: inline-block; padding: 10px 20px; background-color: #007bff; color: #ffffff; text-decoration: none; border-radius: 5px; font-size: 16px;">重置密码</a></p>
        <p style="font-size: 16px; line-height: 1.5; color: #ff1d1d;">
            链接有效时间为15分钟，请及时重置密码。
        </p>
        <p style="font-size: 16px; line-height: 1.5; color: #666666;">
            如果你没有请求找回账号，请忽略这封邮件。
        </p>
        <p style="font-size: 16px; line-height: 1.5; color: #666666;">感谢，</p>
        <p style="font-size: 16px; line-height: 1.5; color: #666666;">Weather Vista团队</p>
    </div>
</body>
</html>
"""

def send_email(rec_emails, subject, content):
    """
    发送电子邮件。

    参数：
        rec_emails (list): 接收者邮箱地址列表。
        subject (str): 邮件主题。
        content (str): 邮件内容，可以是 HTML 格式。
    """
    # 创建多用途的邮件消息
    message = MIMEMultipart()
    # 设置邮件内容为 HTML 格式
    message.attach(MIMEText(content, 'html', 'utf-8'))
    # 邮件主题
    message['Subject'] = subject
    # 发件人
    message['From'] = SENDER_EMAIL
    # 接收者
    message['To'] = ', '.join(rec_emails)

    # 使用 with 语句管理 SMTP 连接，确保连接正确关闭
    try:
        with smtplib.SMTP(MAIL_HOST, 25) as smtp_obj:
            # 登录到服务器
            smtp_obj.login(MAIL_USER, MAIL_PASS)
            # 发送邮件
            smtp_obj.sendmail(SENDER_EMAIL, rec_emails, message.as_string())
        logging.info('Email sent successfully')
    except smtplib.SMTPException as e:
        logging.error(f'Failed to send email: {e}')

def send_find_email(email):
    """
    发送找回账号的电子邮件。

    参数：
        email (str): 接收者的邮箱地址。
    """
    # 重置密码链接
    reset_link = func.generate_reset_link(email)
    # reset_link = 'https://example.com/reset_password?token='
    
    # 格式化最终的 HTML 内容
    content = FIND_HTML_TEMPLATE.format(reset_link=reset_link)
    
    # 发送找回账号的邮件
    send_email([email], '【Weather Vista】账号找回', content)

# 示例使用
if __name__ == '__main__':
    send_find_email("2050791391@qq.com")

from random import Random  # 用于生成随机码
from django.core.mail import send_mail  # 发送邮件模块
from front_end.models import EmailVerifyRecord  # 邮箱验证model
from Blog.settings import EMAIL_FROM  # setting.py添加的的配置信息

# 生成随机字符串
def random_str(randomlength=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str

    # 发送数据加密

def send_email(email, send_type):
    email_record = EmailVerifyRecord()
    # 将给用户发的信息保存在数据库中
    code = random_str(16)
    email_record.code = code
    # 初始化为空
    email_title = ""
    email_body = ""
    # 如果为注册类型
    if send_type == "register":
        email_title = "来自www.chenglinxi.top的注册激活链接"
        email_body = "感谢注册！请点击下面的链接激活你的账号:http:www.chenglinxi.top/active/{0}".format(code)
        # 发送邮件
        try:
            send_mail(email_title, email_body, EMAIL_FROM, [email])
            email_record.email = email
            email_record.send_type = send_type
            email_record.save()
            return 1
        except Exception as e:
            return '邮件发送失败,错误代码为: %s' % e

    # 如果为忘记密码类型
    if send_type == "forget":
        email_title = "来自www.chenglinxi.top的密码找回链接"
        email_body = "感谢您访问本站点！请点击下面的链接跳转到密码找页面:http://www.chenglinxi.top/update_password/{0}".format(code)
        # 发送邮件
        try:
            send_mail(email_title, email_body, EMAIL_FROM, [email])
            email_record.email = email
            email_record.send_type = send_type
            email_record.save()
            return 1
        except Exception as e:
            return '邮件发送失败,错误代码为: %s' % e

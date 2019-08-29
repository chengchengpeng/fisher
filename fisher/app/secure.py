# 涉及安全，如数据库密码，生产环境和工作环境不一样的代码，放入secure
DEBUG = True
SQLALCHEMY_DATABASE_URI = 'mysql+cymysql://root:12345678@localhost:3306/fisher'
SECRET_KEY = '\dfas]fh]mvb]rwe]czx]iuyi\ghdsa'

# email参数
MATL_SERVER = 'smtp.qq.com'
MATL_PORT = 465
MAIL_USE_SSL = True
MAIL_USE_TSL = False
MAIL_USERNAME = '2946430796@qq.com'
MAIL_PASSWORD = ''
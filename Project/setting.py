import os
import sys
import time

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
# SQLite URI compatible
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

today = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time() + 20))

class BaseConfig(object):
    pass
    # SECRET_KEY = os.getenv('SECRET_KEY', 'dev key')
    #
    # DEBUG_TB_INTERCEPT_REDIRECTS = False
    #
    # SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_RECORD_QUERIES = True


class TestingConfig(BaseConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # in-memory database


# 定时任务
class APSchedulerJobConfig(BaseConfig):
    SCHEDULER_API_ENABLED = True
    SCHEDULER_TIMEZONE = 'Asia/Shanghai'
    JOBS = [
        {
            'id': 'No1',  # 任务唯一ID
            'func': 'Project.cron_job.SubscribeToUpdates:update_timer_cron',
            # 执行任务的function名称，app.test 就是 app下面的`test.py` 文件，`shishi` 是方法名称。文件模块和方法之间用冒号":"，而不是用英文的"."
            'args': '',  # 如果function需要参数，就在这里添加
            'trigger': {
              'type': 'cron',           # 类型
              'day_of_week': "0-6",     # 可定义具体哪几天要执行
              'hour': '2',              # 每小时数 , 每天的凌晨2点update
              'minute': '0',
              'second': '0'   # "*/3" 表示每3秒执行一次，单独一个"3" 表示每分钟的3秒。现在就是每一分钟的第3秒时循环执行。
            }
        }
    ]


flask_config = {
    'addJob': APSchedulerJobConfig,
    'testing': TestingConfig,
}

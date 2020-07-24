import inspect
import optparse
import os
import sys
import time

from core.common import check_sudo
from core.compat import xrange
from core.log import create_log_directory, get_error_log_handle
from core.settings import *
from core.update import update_trails
from thirdparty import six
from .cron_job.SubscribeToUpdates import update_timer

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
            # 'trigger': {
            #   'type': 'cron', # 类型
            #    "trigger": "interval",
            #   # 'day_of_week': "0-6", # 可定义具体哪几天要执行
            #   # 'hour': '*', # 小时数
            #   # 'minute': '1',
            #   'second': '*/3600'   # "*/3" 表示每3秒执行一次，单独一个"3" 表示每分钟的3秒。现在就是每一分钟的第3秒时循环执行。
            # }
            'tigger':'interval',
            'second': 60 * 5
        }
    ]
    def __init__(self):
        self.main()
        pass

    def main(self):
        # 判断参数加入问题
        for i in xrange(1, len(sys.argv)):
            if sys.argv[i] == "-q":
                sys.stdout = open(os.devnull, 'w')
            if sys.argv[i] == "-i":
                for j in xrange(i + 2, len(sys.argv)):
                    value = sys.argv[j]
                    if os.path.isfile(value):
                        sys.argv[i + 1] += ",%s" % value
                        sys.argv[j] = ''
                    else:
                        break

        print("%s (sensor) #v%s\n" % (NAME, VERSION))
        # optparse.OptionParser生成符合Unix风格的命令行参数
        parser = optparse.OptionParser(version=VERSION)
        parser.add_option("-c", dest="config_file", default=CONFIG_FILE,
                          help="configuration file (default: '%s')" % os.path.split(CONFIG_FILE)[-1])
        parser.add_option("-i", dest="pcap_file", help="open pcap file for offline analysis")
        parser.add_option("-p", dest="plugins", help="plugin(s) to be used per event")
        parser.add_option("-q", dest="quiet", action="store_true", help="turn off regular output")
        parser.add_option("--console", dest="console", action="store_true",
                          help="print events to console (Note: switch '-q' might be useful)")
        parser.add_option("--no-updates", dest="no_updates", action="store_true",
                          help="disable (online) trail updates")
        parser.add_option("--debug", dest="debug", action="store_true", help=optparse.SUPPRESS_HELP)
        parser.add_option("--profile", dest="profile", help=optparse.SUPPRESS_HELP)
        options, _ = parser.parse_args()  # options中的key是我们需要的参数值，_是args

        read_config(options.config_file)
        # dir()返回类的所有__xx__属性
        for option in dir(options):
            if isinstance(getattr(options, option), (six.string_types, bool)) and not option.startswith('_'):
                config[option] = getattr(options, option)

        if options.debug:
            config.console = True
            config.PROCESS_COUNT = 1
            config.SHOW_DEBUG = True

        if options.pcap_file:
            if options.pcap_file == '-':
                print("[i] using STDIN")
            else:
                for _ in options.pcap_file.split(','):
                    if not os.path.isfile(_):
                        exit("[!] missing pcap file '%s'" % _)

                print("[i] using pcap file(s) '%s'" % options.pcap_file)

        if not config.DISABLE_CHECK_SUDO and not check_sudo():
            exit("[!] please run '%s' with sudo/Administrator privileges" % __file__)

        try:  # 进入初始化模块
            self.init()
        except KeyboardInterrupt:
            print("\r[x] stopping (Ctrl-C pressed)")

    def init(self):
        """
        Performs sensor initialization
        """
        # 创建日志目录逻辑
        create_log_directory()
        # 错误日志逻辑
        get_error_log_handle()

        check_memory()

        msg = "[i] using '%s' for trail storage" % config.TRAILS_FILE
        if os.path.isfile(config.TRAILS_FILE):
            mtime = time.gmtime(os.path.getmtime(config.TRAILS_FILE))
            msg += " (last modification: '%s')" % time.strftime(HTTP_TIME_FORMAT, mtime)

        print(msg)
        # 更新硬盘病毒库
        update_timer()


config = {
    'addJob': APSchedulerJobConfig,
    'testing': TestingConfig,
}

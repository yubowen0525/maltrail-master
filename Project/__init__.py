import atexit
import os
import platform
import sys
import time

import click
from flask import Flask
# from .extension import db
from .extension import api
from .extension import scheduler
from .setting import flask_config
from .get_packet import app_rustful
# from .models import Note
from .models import *

# maltrail 依赖
import optparse
from core.common import check_sudo
from core.compat import xrange
from core.log import create_log_directory, get_error_log_handle
from core.settings import *
from thirdparty import six
from .cron_job.SubscribeToUpdates import update_timer

def creat_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')
    app = Flask(__name__)
    app.config.from_object(flask_config[config_name])
    # register_project_init()
    register_extensions(app)
    register_cronjob(app)
    register_blueprints(app)
    return app


def register_cronjob(app):
    # 保证系统只启动一次定时任务，使用文件锁
    if platform.system() != 'Windows':
        fcntl = __import__("fcntl")
        f = open('scheduler.lock', 'wb')
        # try:
        fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
        scheduler.init_app(app)
        scheduler.start()
        print("scheduler trails update started.")
        # except :
        #     pass

        def unlock():
            fcntl.flock(f, fcntl.LOCK_UN)
            f.close()
        atexit.register(unlock)


def register_extensions(app):
    # db.init_app(app)
    pass

def register_blueprints(app):
    app.register_blueprint(app_rustful)


def register_project_init():
    project_init()

def project_init():
    main()


def main():
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

    print("%s : v%s\n" % (NAME, VERSION))
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

    if not config.DISABLE_CHECK_SUDO and not check_sudo():
        exit("[!] please run '%s' with sudo/Administrator privileges" % __file__)

    try:  # 进入初始化模块
        init()
    except KeyboardInterrupt:
        print("\r[x] stopping (Ctrl-C pressed)")

def init():
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
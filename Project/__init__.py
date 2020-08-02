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
from core.log import create_log_directory, get_error_log_handle, log_error
from core.settings import *
from core.settings import maltrail_config as maltrail_config
from thirdparty import six
from .cron_job.SubscribeToUpdates import update_timer, cron_job_load_trails


def creat_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')
    app = Flask(__name__)
    app.config.from_object(flask_config[config_name])
    register_project_init()
    register_extensions(app)
    register_cronjob(app)
    register_blueprints(app)
    return app


def register_cronjob(app):
    # 保证系统只启动一次定时任务，使用文件锁
    scheduler.init_app(app)
    scheduler.start()
    print("scheduler job started.")
    log_error("scheduler job started.","INFO")


def register_extensions(app):
    # db.init_app(app)
    pass


def register_blueprints(app):
    app.register_blueprint(app_rustful)


def register_project_init():
    print("%s : v%s\n" % (NAME, VERSION))
    init_config()
    project_init()
    cron_job_load_trails()
    log_error("init success", "INFO")

def init_config():
    read_config(CONFIG_FILE)

def project_init():
    if not maltrail_config.DISABLE_CHECK_SUDO and not check_sudo():
        exit("[!] please run '%s' with sudo/Administrator privileges" % __file__)

    try:  # 进入初始化模块
        init()
        get_error_log_handle()
        msg = "[i] using '%s' for trail storage" % maltrail_config.TRAILS_FILE
        if os.path.isfile(maltrail_config.TRAILS_FILE):
            mtime = time.gmtime(os.path.getmtime(maltrail_config.TRAILS_FILE))
            msg += " (last modification: '%s')" % time.strftime(HTTP_TIME_FORMAT, mtime)

        log_error(msg, "INFO")
    except KeyboardInterrupt:
        print("\r[x] stopping (Ctrl-C pressed)")


def init():
    """
    Performs sensor initialization
    """
    # 创建日志目录逻辑
    create_log_directory()
    # 错误日志逻辑
    check_memory()

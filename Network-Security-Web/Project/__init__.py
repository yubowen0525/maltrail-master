import atexit
import os
import platform

import click
from flask import Flask
# from .extension import db
from .extension import api
from .extension import scheduler
from .setting import config
from .get_packet import app_rustful
# from .models import Note
from .models import *


def creat_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    register_extensions(app)
    register_cronjob(app)
    register_blueprints(app)
    return app


def register_cronjob(app):
    # 保证系统只启动一次定时任务，使用文件锁
    if platform.system() != 'Windows':
        fcntl = __import__("fcntl")
        f = open('scheduler.lock', 'wb')
        try:
            fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
            scheduler.init_app(app)
            scheduler.start()
            print("scheduler started.")
        except:
            pass

        def unlock():
            fcntl.flock(f, fcntl.LOCK_UN)
            f.close()
        atexit.register(unlock)


def register_extensions(app):
    # db.init_app(app)
    pass

def register_blueprints(app):
    app.register_blueprint(app_rustful)

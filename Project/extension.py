# from flask_sqlalchemy import SQLAlchemy
from apscheduler.executors.pool import ProcessPoolExecutor
from apscheduler.schedulers.background import BackgroundScheduler
from flask_restful import Api
from flask_apscheduler import APScheduler

# db = SQLAlchemy()
api = Api()
# scheduler = APScheduler()
executors = {
      'default': ProcessPoolExecutor(5) # 最多5个进程同时执行
  }
scheduler = APScheduler(BackgroundScheduler(timezone="Asia/Shanghai",executors=executors))
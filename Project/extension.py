# from flask_sqlalchemy import SQLAlchemy
from apscheduler.schedulers.background import BackgroundScheduler
from flask_restful import Api
from flask_apscheduler import APScheduler

# db = SQLAlchemy()
api = Api()
# scheduler = APScheduler()
scheduler = APScheduler(BackgroundScheduler(timezone="Asia/Shanghai"))
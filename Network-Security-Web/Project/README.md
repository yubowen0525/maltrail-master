# Project
##  __init__.py
- create_app():  创建一个app对象  app = Flask(__name__)
- register_*****(): 将extension创建的对象使用init_app()函数注册到app


# extension
## flask_restful
[官网](https://flask-restful.readthedocs.io/en/latest/)
## flask_sqlalchemy
[官网](http://www.pythondoc.com/flask-sqlalchemy/quickstart.html)

# setting
app.config.from_object(config[config_name]) 
基于class 的导入app实例配置文件。
目前项目没有用到，留作后面扩展使用
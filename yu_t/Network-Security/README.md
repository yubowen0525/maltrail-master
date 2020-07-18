# 环境安装
## 安装flask环境需求
```shell script
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

# 启动
## 方式1 wsgi web 启动 测试使用
```shell script
python3 wsgi.py
```


## 方式2 工业环境启动
```shell script
gunicorn wsgi:app -c ./gunicorn.conf.py
```

## 方式3 Docker启动
```shell script
docker build -t="flask-web:v1.0" .
docker images
docker run -d flask-web:v1.0 /bin/bash
```

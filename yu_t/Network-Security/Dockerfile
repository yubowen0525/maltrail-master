FROM python:3.6
# 构建在服务器上的工作路径
WORKDIR /Project/demo

# 拷贝本地文件到镜像中
COPY requirements.txt ./
# 构建镜像需要执行的操作
RUN pip install -r requirements.txt

COPY ./Project ./
COPY ./wsgi.py ./

# CMD ["gunicorn","wsgi:app","-c","./gunicorn.conf.py"]
CMD ["flask","run","--host=0.0.0.0","--port=80"]
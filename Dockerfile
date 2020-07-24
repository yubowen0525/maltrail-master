FROM python:3.6
# 构建在服务器上的工作路径
WORKDIR /Project/demo

ENV PATHONPATH /Project/demo/
# 拷贝本地文件到镜像中
COPY ./ ./

# 构建镜像需要执行的操作
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple




# CMD ["gunicorn","wsgi:app","-c","./gunicorn.conf.py"]
CMD ["flask","run","--host=0.0.0.0","--port=80"]
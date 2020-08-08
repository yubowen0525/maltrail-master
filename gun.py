import os
import time

import gevent.monkey

gevent.monkey.patch_all()

import multiprocessing

# 监听本机的5000端口
bind = '0.0.0.0:25000'
timeout = 300
# 开启4个进程
# workers = 4
# 线程
# threads=8000
# keepalive = 1
# 在keep-alive连接上等待请求的秒数，默认情况下值为2。一般设定在1~5秒之间。
# 设置守护进程,将进程交给supervisor管理
daemon = False
worker_connections = 8048
# worker_connections最大客户端并发数量，默认情况下这个值为1000。此设置将影响gevent和eventlet工作模式
graceful_timeout = 10
# graceful_timeout优雅的人工超时时间，默认情况下，这个值为30。收到重启信号后，工作人员有那么多时间来完成服务请求。在超时(从接收到重启信号开始)之后仍然活着的工作将被强行杀死
limit_request_line = 8048
# limit_request_line HTTP请求行的最大大小，此参数用于限制HTTP请求行的允许大小，默认情况下，这个值为4094。值是0~8190的数字。此参数可以防止任何DDOS攻击
# 监听队列
backlog = 8048
# 工作模式为gevent
# worker_class = "gevent"
debug = True
proc_name = 'gunicorn.pid'
# 记录PID
pidfile = 'debug.log'
# access_log_format = '%(t)s %(p)s %(h)s "%(r)s" %(s)s %(L)s %(b)s %(f)s" "%(a)s"'
# 设置gunicorn访问日志格式，错误日志无法设置
# errorlog = "./gunicorn-errlog"
# accesslog = "./gunicorn-logs"

logconfig_dict = {
    'version': 1,
    'disable_existing_loggers': False,
    'loggers': {
        "gunicorn.error": {
            "level": "INFO",  # 打日志的等级可以换的，下面的同理
            "handlers": ["error_file"],  # 对应下面的键
            "propagate": 1,
            "qualname": "gunicorn.error"
        },

        "gunicorn.access": {
            "level": "INFO",
            "handlers": ["access_file"],
            "propagate": 0,
            "qualname": "gunicorn.access"
        }
    },
    'handlers': {
        'console': {
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
            'formatter': 'generic',
            # 'propagate': False
        },
        "error_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "maxBytes": 1024 * 1024 * 1024,  # 打日志的大小，我这种写法是1个G
            "backupCount": 1,  # 备份多少份，经过测试，最少也要写1，不然控制不住大小
            "formatter": "generic",  # 对应下面的键
            # 'mode': 'w+',
            "filename": "/var/log/maltrail1/gunicorn/gunicorn.error.log"  # 打日志的路径
        },
        "access_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "maxBytes": 1024 * 1024 * 1024,
            "backupCount": 1,
            "formatter": "generic",
            "filename": "/var/log/maltrail1/gunicorn/gunicorn.access.log",
        }
    },
    'formatters': {
        "generic": {
            "format": "'[%(process)d] [%(asctime)s] %(levelname)s [%(filename)s:%(lineno)s] %(message)s'",  # 打日志的格式
            "datefmt": "[%Y-%m-%d %H:%M:%S %z]",  # 时间显示方法
            "class": "logging.Formatter"
        },
        "access": {
            "format": "'[%(process)d] [%(asctime)s] %(levelname)s [%(filename)s:%(lineno)s] %(message)s'",
            "class": "logging.Formatter"
        }
    }
}

# 启动的进程数
workers = 4
# workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'gunicorn.workers.ggevent.GeventWorker'

x_forwarded_for_header = 'X-FORWARDED-FOR'

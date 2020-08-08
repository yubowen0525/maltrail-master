import sys


def add_path():
    path = sys.argv[0]
    pathList = path.split('/')
    for i in range(1, 4):
        path = "/".join(pathList[0:-i])
        sys.path.append(path)


add_path()

from Project import init_config, init
from Project.cron_job.SubscribeToUpdates import update_timer


def start_update_trails():
    add_path()
    init_config()
    init()
    update_timer()


if __name__ == '__main__':
    start_update_trails()

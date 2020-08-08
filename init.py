from Project import init_config, init
from Project.cron_job.SubscribeToUpdates import update_timer


def start_update_trails():
    init_config()
    init()
    update_timer()


if __name__ == '__main__':
    start_update_trails()

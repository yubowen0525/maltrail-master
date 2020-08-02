from Project import init_config,init
from Project.cron_job.SubscribeToUpdates import update_timer


if __name__ == '__main__':
    init_config()
    init()
    update_timer()
import platform

from Project import init_config, init
from Project.cron_job.SubscribeToUpdates import update_timer


def start_update_trails():
    init_config()
    init()
    update_timer()

def update_timer_cron():
    if platform.system() != 'Windows':
        fcntl = __import__("fcntl")
        f = open('scheduler.lock', 'wb')
        try:
            def unlock():
                fcntl.flock(f, fcntl.LOCK_UN)
                f.close()
            fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
            # log_error("cron_job start update_trail", "INFO")
            # read_config(CONFIG_FILE)
            update_timer()
            unlock()
        except :
            pass

if __name__ == '__main__':
    # update_timer_cron()
    start_update_trails()

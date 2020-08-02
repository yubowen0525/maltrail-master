import platform
import time

from core.common import load_trails, check_connection
from core.log import log_error
from core.settings import *
from core.settings import maltrail_config as config
from core.update import update_trails


def update_timer():
    retries = 0
    if not config.no_updates:  # 判断是否设置不更新，然后会利用抓取页面检测网络状态
        while retries < CHECK_CONNECTION_MAX_RETRIES and not check_connection():
            sys.stdout.write(
                "[!] can't update because of lack of Internet connection (waiting..." if not retries else '.')
            sys.stdout.flush()
            log_error("[!] can't update because of lack of Internet connection (waiting...", "Warning")
            time.sleep(10)
            retries += 1

        if retries:
            print(")")
    # 超出次数，那么使用update_trails的离线模式
    if config.no_updates or retries == CHECK_CONNECTION_MAX_RETRIES:
        if retries == CHECK_CONNECTION_MAX_RETRIES:
            print("[x] going to continue without online update")
            log_error("[x] going to continue without online update", "Warning")
        _ = update_trails(offline=True)
    else:  # 正常进入
        _ = update_trails()
        # update_ipcat()
    # 有新的trails
    if _:
        trails.clear()
        trails.update(_)
    elif not trails:    # load_trails()只是加载trails()进内存
        _ = load_trails()
        trails.update(_)

    _regex = ""
    for trail in trails:
        if "static" in trails[trail][1]:
            if re.search(r"[\].][*+]|\[[a-z0-9_.\-]+\]", trail, re.I):
                try:
                    re.compile(trail)
                except:
                    pass
                else:
                    if re.escape(trail) != trail:
                        index = _regex.count("(?P<g")
                        if index < 100:  # Reference: https://stackoverflow.com/questions/478458/python-regular-expressions-with-more-than-100-groups
                            _regex += "|(?P<g%s>%s)" % (index, trail)

    trails._regex = _regex.strip('|')

def update_timer_cron():
    if platform.system() != 'Windows':
        fcntl = __import__("fcntl")
        f = open('scheduler.lock', 'wb')
        try:
            def unlock():
                fcntl.flock(f, fcntl.LOCK_UN)
                f.close()
            fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
            log_error("cron_job start update_trail", "INFO")
            update_timer()
            unlock()
        except :
            pass



def cron_job_load_trails():
    '''
    重新加载trails到内存
    :return:
    '''
    _ = load_trails()
    trails.update(_)

    _regex = ""
    for trail in trails:
        if "static" in trails[trail][1]:
            if re.search(r"[\].][*+]|\[[a-z0-9_.\-]+\]", trail, re.I):
                try:
                    re.compile(trail)
                except:
                    pass
                else:
                    if re.escape(trail) != trail:
                        index = _regex.count("(?P<g")
                        if index < 100:  # Reference: https://stackoverflow.com/questions/478458/python-regular-expressions-with-more-than-100-groups
                            _regex += "|(?P<g%s>%s)" % (index, trail)

    trails._regex = _regex.strip('|')
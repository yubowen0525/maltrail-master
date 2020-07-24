#!/usr/bin/env python
# coding=utf-8

"""
Copyright (c) 2014-2020 Maltrail developers (https://github.com/stamparm/maltrail/)
See the file 'LICENSE' for copying permission
"""

import os
import struct
import threading
import time

from core.common import load_trails
from core.enums import BLOCK_MARKER
from core.settings import BLOCK_LENGTH
from core.settings import config
from core.settings import LOAD_TRAILS_RETRY_SLEEP_TIME
from core.settings import REGULAR_SENSOR_SLEEP_TIME
from core.settings import SHORT_SENSOR_SLEEP_TIME
from core.settings import trails

def read_block(buffer, i):
    offset = i * BLOCK_LENGTH % config.CAPTURE_BUFFER

    while True:
        if buffer[offset] == BLOCK_MARKER.END:
            return None

        while buffer[offset] == BLOCK_MARKER.WRITE:
            time.sleep(SHORT_SENSOR_SLEEP_TIME)

        buffer[offset] = BLOCK_MARKER.READ
        buffer.seek(offset + 1)

        length = struct.unpack("=H", buffer.read(2))[0]
        retval = buffer.read(length)

        if buffer[offset] == BLOCK_MARKER.READ:
            break

    buffer[offset] = BLOCK_MARKER.NOP
    return retval

def write_block(buffer, i, block, marker=None):
    offset = i * BLOCK_LENGTH % config.CAPTURE_BUFFER

    while buffer[offset] == BLOCK_MARKER.READ:
        time.sleep(SHORT_SENSOR_SLEEP_TIME)

    buffer[offset] = BLOCK_MARKER.WRITE
    buffer.seek(offset + 1)
    buffer.write(struct.pack("=H", len(block)) + block)
    buffer[offset] = marker or BLOCK_MARKER.NOP

def worker(buffer, n, offset, mod, process_packet):
    '''
    Worker process used in multiprocessing mode
    :param buffer: mmap共享内存地址
    :param n: Value创建对象，一般用于进程通信
    :param offset: i，第几个线程，取值范围：0-6
    :param mod: 7,配置信息创建几个线程
    :param process_packet: 函数地址，处理数据包的回调函数
    :return:
    '''

    def update_timer():
        # 查看trail.csv的上一次修改时间，差1天更新，其实这里的trails已经在初始化阶段加入了trail.csv的内容。
        # **只是利用这个函数来读取trail.csv的新内容**
        # 因为只是读，所以没有加锁。所以主线程1天更新一次，多线程采用读来同步trails的状态。
        if (time.time() - os.stat(config.TRAILS_FILE).st_mtime) >= config.UPDATE_PERIOD:
            _ = None
            while True:
                _ = load_trails(True)
                if _:
                    trails.clear()
                    trails.update(_)
                    break
                else:
                    time.sleep(LOAD_TRAILS_RETRY_SLEEP_TIME)
        # 1天后再次执行
        threading.Timer(config.UPDATE_PERIOD, update_timer).start()

    update_timer()

    count = 0
    while True:
        try:
            # 将count取余后对上线程的i标志
            if (count % mod) == offset:
                # n.value用于同步？
                if count >= n.value:
                    time.sleep(REGULAR_SENSOR_SLEEP_TIME)
                    continue
                # 获取到包内容，如果把mmap比喻成一个队列，那么7个线程以i=0的线程为例，就会去取mmap的第0,7,14,21,28的内容
                content = read_block(buffer, count)

                if content is None:
                    break

                elif len(content) < 12:
                    continue
                # 这里的i解出来是unsignedint
                sec, usec, ip_offset = struct.unpack("=III", content[:12])
                packet = content[12:]
                process_packet(packet, sec, usec, ip_offset)

            count += 1

        except KeyboardInterrupt:
            break

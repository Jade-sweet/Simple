import json
import os
import time
from queue import Queue
from threading import RLock

from my_lib.code_encryption import obj_decode


class Task:

    def __init__(self, house_type, area):
        self.house_type = house_type
        self.area = area


# 单例装饰器
def singleton(cls):
    instance = {}
    lock = RLock()

    def wrapper(*args, **kwargs):
        if cls not in instance:
            with lock:
                if cls not in instance:
                    instance[cls] = cls(*args, **kwargs)
        return instance[cls]
    return wrapper


@singleton
class TaskQueue:
    def __init__(self, max_size=128):
        self.max_size = max_size
        self.queue = Queue(maxsize=max_size)

    @property
    def is_full(self):
        return self.queue.full()

    @property
    def spare_size(self):
        return self.max_size - self.queue.qsize()

    @property
    def has_size(self):
        return self.queue.qsize()

    @property
    def pop(self):
        """取出任务"""
        return self.queue.get()

    def push(self, task: Task):
        """追加任务"""
        self.queue.put(task)


def run_crawler(task: Task):
    """运行爬虫"""
    SPIDER_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print(SPIDER_DIR)
    os.chdir(SPIDER_DIR)
    # 放开以下注释，即可启动真实爬虫，但是该爬虫并不完善
    # os.system('scrapy crawl spider -a house_type=%s -a area=%s' % (task.house_type, task.area))
    print(f'正在运行新爬虫')
    time.sleep(10)
    print(f'爬虫运行结束')
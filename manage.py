#!/usr/bin/env python
import os
import sys
import threading

from my_lib.tasks import TaskQueue, run_crawler


def spider_thread():
    while True:
        task = TaskQueue().pop
        run_crawler(task)


if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'simple_crawler_service.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    t1 = threading.Thread(target=spider_thread, args=())
    t1.start()
    execute_from_command_line(sys.argv)

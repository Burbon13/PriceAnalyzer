import threading

import time

from threading_manager.TaskResult import TaskResult
from threading_manager.TaskType import TaskType


class MonitorProductsTask(threading.Thread):
    def __init__(self, queue, service):
        threading.Thread.__init__(self)
        self.queue = queue
        self.service = service

    def run(self):
        try:
            self.service.monitor()
            # time.sleep(4)
            self.queue.put((TaskType.SCAN, TaskResult.OKAY, None))
        except Exception as e:
            self.queue.put((TaskType.SCAN, TaskResult.ERROR, e))

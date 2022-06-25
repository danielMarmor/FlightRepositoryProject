import threading
import time


class PoolCorrelationEvents:
    def __init__(self, max_size):
        self.events = {}
        self.max_size = max_size
        # self.lock = threading.Lock()
        self.lock_add = threading.Lock()
        self.lock_signal = threading.Lock()
        # self.lock_remove = threading.RLock()

    def add(self, correl_obj, correlation_id):
        self.events[correlation_id] = correl_obj
        wait = correl_obj['event'].wait()
        return wait

    def signal(self, correlation_id, response, exception):
        while True:
            correlation = correlation_id in self.events.keys()
            if correlation:
                break
            time.sleep(0.01)
        # SIGNAL
        correl_obj = self.events[correlation_id]
        if response is not None:
            correl_obj['response'] = response
        if exception is not None:
            correl_obj['exception'] = exception
        event = correl_obj['event']
        event.set()

    def remove(self, correlation_id):
        if correlation_id not in self.events.keys():
            raise Exception(f'correlation_id {correlation_id} not exists')
        self.events.pop(correlation_id)



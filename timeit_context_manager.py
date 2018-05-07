from datetime import datetime

class timeit(object):
    def __init__(self, name):
        self.name = name

    def __enter__(self):
        self.start = datetime.now()

    def __exit__(self, exc_type, exc_val, exc_tb):
        log.info("{} {}ms".format(self.name, datetime.now() - self.start))

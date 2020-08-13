import signal
import time
import logging
import sys
import random
import multiprocessing as mp

from concurrent import futures


class Handler:

    STOP = False
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        log_format = "%(asctime)-15s %(levelname)s: %(message)s"
        formatter = logging.Formatter(log_format)
        hdlr = logging.StreamHandler(sys.stdout)
        hdlr.setFormatter(formatter)
        self.logger.addHandler(hdlr)
        self.logger.setLevel(logging.DEBUG)
    
    def start_proccess(self, x):
        self.logger.debug("Iniciando processo %s" % x)
        self.signal_handler()
        process = mp.Process(target=self.start_thread, args=(x,))
        process.start()

    def start_thread(self, x):
        threads = []
        self.logger.debug("Iniciando threads")
        max_workers = 4
        with futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            self.logger.debug("Começando threads")
            for y in range(max_workers):
                response = executor.submit(self.thread_task, x=x, y=y + 1)
                threads.append(response)

    def thread_task(self, x, y):
        tempo = random.randint(5, 15)
        self.logger.debug("Rodando thread %s por %s segundos" % (y, tempo))
        time.sleep(tempo)
        self.logger.debug("Saindo da thread %s e do processo %s" % (y, x))

    def signal_handler(self):

        signal.signal(signal.SIGTERM, self.sigterm)
        signal.signal(signal.SIGINT, self.sigint)

    def sigterm(self, signum, frame):
        self.logger.debug("SIGTERM!!!!")
        self.STOP = True

    def sigint(self, signum, frame):
        self.logger.debug("SIGINT %s" % signum)
        self.STOP = True

    def start(self):
        count = 1
        while not h.STOP:
            h.start_proccess(count)
            count += 1
            time.sleep(3)
        self.logger.debug("ACABOUUUUUUUUUUUUUUUU!!!!!")


if __name__ == '__main__':
    h = Handler()
    h.logger.debug("Esperando signal...")
    h.start()

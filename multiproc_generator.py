import time
import datetime
from multiprocessing import Process, Value, JoinableQueue


class Consumer(Process):
    def __init__(self, work_queue):
        Process.__init__(self)
        self._work_queue = work_queue
        self._counter = Value('i', 0)

    def run(self):
        while True:
            try:
                item = self._work_queue.get()
                self._counter.value += 1
                a = (len(item)) ** 2
                for _ in range(20000):
                    _ = 0
            except Exception as v:
                print(str(v))
            finally:
                # now = datetime.datetime.now()
                # print('{0}. Finished at: {1}'.format(self.getName(), now))
                self._work_queue.task_done()

    def get_counter(self):
        # print(self.name, self._counter.value, 'FUNC', self._work_queue.qsize(), self.pid)
        return self._counter.value


class Producer(Process):
    def __init__(self, generate_queue, work_queue):
        Process.__init__(self)
        self._generate_queue = generate_queue
        self._work_queue = work_queue

    def run(self):
        while True:
            try:
                self._generate_queue.get()
                now = datetime.datetime.now()
                # print('Started generate    ', now)
                # for _ in range(25000):
                    # now = datetime.datetime.now()
                with open('C:\\cities.txt', 'r') as f:
                    self._work_queue.put(f.read())
                    # print(f)
                # if _ % 5000 == 0:
                #     print(_)
            finally:
                self._generate_queue.task_done()


def get_workers_status(worker_list):
    for process in worker_list:
        # print(worker_list)
        process.get_counter()
        # print(type(process))
        print(process.name, process.get_counter())


def main():
    work_queue = JoinableQueue(maxsize=500)
    generate_queue = JoinableQueue()

    worker_list = []
    generator_list = []

    now = datetime.datetime.now()
    print('Started generate    ', now)

    for _ in range(8):
        generator = Producer(generate_queue, work_queue)
        generator.daemon = True
        generator.start()
        generator_list.append(generator)

    for _ in range(8):
        worker = Consumer(work_queue)
        worker.daemon = True
        worker.start()
        worker_list.append(worker)

    for _ in range(100000):
        generate_queue.put('')

    while not work_queue.empty() or not generate_queue.empty():
        get_workers_status(worker_list=worker_list)
        # for process in worker_list:
        #     # print(type(process))
        #     print(process.name, process.get_counter())
        time.sleep(3)
    print('last')
    get_workers_status(worker_list=worker_list)

    generate_queue.join()
    work_queue.join()

    now = datetime.datetime.now()
    print('Finished all processes at: {}'.format(now))

if __name__ == '__main__':
    main()

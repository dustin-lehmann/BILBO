import time

from utils.callbacks import Callback
from utils.thread_worker import ThreadWorker, WorkerPool
from utils.events import EventListener


def testfunction1(input: int, *args, **kwargs):
    # raise Exception("Test Exception")
    # if input == 5:
    #     time.sleep(3)
    return input*2


def listener_callback(*args, **kwargs):
    print("Listener callback")


def main():
    num_workers = 10
    workers = []

    for i in range(0, num_workers):
        workers.append(ThreadWorker(start=False, function=Callback(function=testfunction1, parameters={'input': i})))

    pool = WorkerPool(workers)
    pool.start()

    results = pool.wait(timeout=0.1)
    data = pool.get_data()
    print(f"Run Time: {pool.run_time} ms")
    if all(results):
        print(f"All workers finished in time: {results}")
        print(f"Errors: {pool.errors}")
        print(f"Data: {data}")
    else:
        print(f"Not all workers finished successfully: {results}")
        print(f"Errors: {pool.errors}")
        print(f"Data: {data}")

    # worker = ThreadWorker(function=Callback(function=testfunction1, parameters={'input': 1}), start=False)
    # listener = EventListener(worker.event, callback=listener_callback, once=False)
    # listener.start()
    # worker.start()
    #
    # if worker.wait(timeout=1):
    #     print("Success")
    # else:
    #     print("Timed out")

    # workers = []
    #
    # for i in range(0, 10):
    #     workers.append(ThreadWorker(function=Callback(function=testfunction1, parameters={'input': i})))
    #
    # for i in range(0, 10):
    #     if workers[i].wait(timeout=1):
    #         print(f"Worker {i} success")
    #     else:
    #         print(f"Worker {i} timed out")


if __name__ == '__main__':
    main()

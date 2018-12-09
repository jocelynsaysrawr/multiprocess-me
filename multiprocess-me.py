import time
import random

from multiprocessing import Process, Queue, current_process, freeze_support

# function run by worker processes
def worker(input, output):
    for func, args in iter(input.get, 'STOP'):
        result = calculate(func, args)
        output.put(result)

# function used to calculate result
def calculate(func, args):
    result = func(*args)
    return '{} says that {}{} = {}'.format(current_process().name, func.__name__, args, result)

# functions referenced by tasks
def mul(a, b):
    time.sleep(0.5*random.random())
    return a * b

def plus(a, b):
    time.sleep(0.5*random.random())
    return a + b


def test():
    NUMBER_OF_PROCESSES = 4
    TASKS1 = [(mul, (i, 7)) for i in range(20)]
    TASKS2 = [(plus, (i, 8)) for i in range(10)]

    # create queues
    task_queue = Queue()
    done_queue = Queue()

    # submit tasks
    for task in TASKS1:
        task_queue.put(task)

    # start worker processes
    for i in range(NUMBER_OF_PROCESSES):
        Process(target=worker, args=(task_queue, done_queue)).start()

    # get and print results
    print('Unordered results:')
    for i in range(len(TASKS1)):
        print('\t', done_queue.get())

    # add more tasks using `put()`
    for task in TASKS2:
        task_queue.put(task)

    # get and print some more results
    for i in range(len(TASKS2)):
        print('\t', done_queue.get())

    # tell child processes to stop
    for i in range(NUMBER_OF_PROCESSES):
        task_queue.put('STOP')


def main():
    freeze_support()
    test()


if __name__ == '__main__':
    main()

    
import time
import random
import argparse
import requests
import logging
import sys
import os
import signal

from multiprocessing import Process, Queue, current_process, freeze_support
from bs4 import BeautifulSoup

# global variables
DOMAIN_LIST = [
    'google.com', 'devleague.com','google.com', 'devleague.com','google.com', 'devleague.com','google.com', 'devleague.com','google.com', 'devleague.com','google.com', 'devleague.com','google.com', 'devleague.com','google.com', 'devleague.com','google.com', 'devleague.com','google.com', 'devleague.com','google.com', 'devleague.com','google.com', 'devleague.com','google.com', 'devleague.com','google.com', 'devleague.com','google.com', 'devleague.com','google.com', 'devleague.com','google.com', 'devleague.com','google.com', 'devleague.com','google.com', 'devleague.com','google.com', 'devleague.com','google.com', 'devleague.com','google.com', 'devleague.com','google.com', 'devleague.com','google.com', 'devleague.com','google.com', 'devleague.com','google.com', 'devleague.com','google.com', 'devleague.com','google.com', 'devleague.com','google.com', 'devleague.com','google.com', 'devleague.com','google.com', 'devleague.com','google.com', 'devleague.com']
PIDS = []

# commandline options
def usage():
    parser = argparse.ArgumentParser(description='Multiprocess Me: Performance Optimized Web Scraper')
    args = parser.parse_args()

# function run by worker processes
def worker(input, output):
    for func, args in iter(input.get, 'STOP'):
        result = calculate(func, args)
        output.put(result)
        logging.basicConfig(filename='test.log', level=logging.INFO)
        logging.info('\t' + output.get())

# function to add a domain name
def add_domain(domain):
    global DOMAIN_LIST
    if domain in DOMAIN_LIST:
        print('Domain has already been added.')
    else:
        DOMAIN_LIST.append(domain)
        print('{} has been added to list of domains.'.format(domain))

# function used to calculate result
def calculate(func, args):
    result = func(args)
    return '{}:{}:{} contains links to - {}'.format(current_process().name, func.__name__, args, result)

# functions referenced by tasks
def get_url(url):
    r = requests.get('https://' + url)
    soup = BeautifulSoup(r.text, 'html.parser')
    links = []
    for link in soup.find_all('a'):
        links.append(link.get('href'))
    return links  

def test():
    global DOMAIN_LIST
    global PIDS
    NUMBER_OF_PROCESSES = 4
    TASKS1 = [(get_url, (domain)) for domain in DOMAIN_LIST]
    # create queues
    TASK_QUEUE = Queue()
    DONE_QUEUE = Queue()
    
    # submit tasks
    for task in TASKS1:
        TASK_QUEUE.put(task)

    # start worker processes
    for i in range(NUMBER_OF_PROCESSES):
        P = Process(target=worker, args=(TASK_QUEUE, DONE_QUEUE))
        P.start()
        PIDS.append(P.pid)
    
    # tell child processes to stop
    for i in range(NUMBER_OF_PROCESSES):
        TASK_QUEUE.put('STOP')
    

# function to display menu options
def menu_list():
    global DOMAIN_LIST

    try:
        print('\033[1;36;40mPlease choose from the following options:')
        print('\n1. Add a domain name to queue (do not include https:// or http://')
        print('2. View list of domains in queue')
        print('3. Start processing domain queue')
        print('4. Stop processing domain queue')
        print('5. Exit')
        print('\n')
        selection = int(input('\033[1;32;40mSelect option: '))

        if selection == 1:
            domain = input('domain name: ')
            add_domain(domain)
            menu_list()
        if selection == 2:
            print('\n', DOMAIN_LIST)
            menu_list()
        if selection == 3:
            print('\n\033[1;33;40mStarting web crawler \U0001F44C')
            freeze_support()
            test()
            menu_list()
        if selection == 4:
            for pid in PIDS[:]:
                os.kill(pid, signal.SIGTERM)
                print('process terminated: ', pid)
                PIDS.remove(pid)
            menu_list()
        if selection == 5:
            print('\n\033[1;37;41mByeeeee!')
            exit()
    
    except KeyboardInterrupt:
        print('\nExiting...')


def main():
    get_url('google.com')
    usage()
    menu_list()


if __name__ == '__main__':
    main()


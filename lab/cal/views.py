import threading
from django.http import JsonResponse
from random import uniform
from math import sqrt
from threading import Thread
from time import sleep, time
import logging

from ulid import ULID

'''
listando: curl http://localhost:8000/norm/

registrando tarefa: curl http://localhost:8000/norm/1000000000/
'''



logger = logging.getLogger('__name__')

task_queue = []

class NormError(Exception): ...

class EmpetyQueueError(Exception): ...


class Task:

    def __init__(self, size):
        self.id = str(ULID())
        self.size = size
        self.status = 'Scheduled'
        self.result = None
        self.time = None

    def to_dict(self):
        return {
            'id': str(self.id),
            'size': self.size,
            'status': self.status,
            'result': self.result,
            'time': self.time,
        }


class Queue:

    def __init__(self):
        self._tasks_to_do = []
        self._tasks_running = []
        self._tasks_processed = []
        self._start_threads = False

    def find(self, id):
        for t in self._tasks:
            if t.id == id:
                return t

    def all(self):
        return [t.to_dict() for t in self._tasks_to_do + self._tasks_processed + self._tasks_running]

    def start_threads(self, number_of_threads=2):
        self._start_threads = True
        for _ in range(number_of_threads):
            Thread(target=consumer, args=(tasks,)).start()

    @property
    def there_are_no_thread_yet(self):
        return not self._start_threads

    @property
    def tasks_todo(self):
        return self._tasks_to_do

    @property
    def tasks_running(self):
        return self._tasks_running

    def register(self, task):
        self._tasks_to_do.append(task)

    def processed(self, task):
        self._tasks_running.remove(task)
        self._tasks_processed.append(task)

    def get_new_tasks(self):
        try:
            task = self._tasks_to_do.pop()
            self._tasks_running.append(task)
            return task
        except IndexError:
            raise EmpetyQueueError


tasks = Queue()

def consumer(tasks):
    while True:
        logger.info('Quantidade de tasks todo: %d' % len(tasks.tasks_todo))
        logger.info('Quantidade de tasks runnning: %d' % len(tasks.tasks_running))
        try:
            task = tasks.get_new_tasks()

            init = time()
            worker(task)
            task.time = time() - init

            tasks.processed(task)
        except EmpetyQueueError:
            sleep(10)
            continue


def worker(task):
    task.status = 'running ...'
    try:
        result = norm(size=task.size)
        task.result = result
        task.status = 'done'
    except NormError:
        task.status = 'fail.'


def norm(size=10000):

    if size == 101:
        raise NormError

    x = (uniform(-0.1, 0.1) for _ in range(size))

    return sqrt(sum(a**2 for a in x))


def register(request, size):

    if tasks.there_are_no_thread_yet:
        tasks.start_threads()

    task = Task(size)
    tasks.register(task)
    return JsonResponse({'task_id': task.id})


def list_tasks(request):

    logger.warning('Quantidade de tasks runnning: %d' % len(tasks.tasks_running))
    list_ = tasks.all()

    return JsonResponse({'result': list_})


def number_of_threads(request):
    return JsonResponse({'threads_number': threading.active_count()})

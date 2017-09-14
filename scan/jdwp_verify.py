import Queue
import threading
import time
queue = Queue.Queue()
locker = threading.Lock()
Thread_num = 2

class ThreadNum(threading.Thread):
	"""docstring for ThreadNum"""
	def __init__(self, queue):
		threading.Thread.__init__(self)
		self.queue = queue
	def run(self):
		while True:
			try:
				if queue.empty():break
				current_task = self.queue.get()
			except:
				break
			log(current_task)

def add_task(tasks):
	for i in range(0,len(tasks)):
		queue.put(tasks[i])
def log(info):
	locker.acquire()
	print info
	locker.release()
def t_join(t_num):
	while  True:
		time.sleep(1)
		ac_num = threading.activeCount()
		if ac_num <= 1 or queue.empty():
			break

if __name__ == '__main__':
	tasks = ['1234','5678','233333','5555','QAQAQAQ']
	add_task(tasks)
	for i in range(0,Thread_num):
		t = ThreadNum(queue)
		t.setDaemon(True)
		t.start()
	t_join(Thread_num)

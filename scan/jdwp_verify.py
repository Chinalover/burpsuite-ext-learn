import Queue
import threading
import time
import socket
import sys
queue = Queue.Queue()
locker = threading.Lock()
Thread_num = 20
HANDSHAKE = "JDWP-Handshake"
TIMEOUT = 5

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
			host,port = current_task.split(":")
			port = int(port)
			s = socket.socket()
			try:
				log('testing %s:%s ....' % (host,str(port)))
				s.connect( (host, port) )
				s.send( HANDSHAKE )
				hand_msg = s.recv( len(HANDSHAKE) )
				if hand_msg != HANDSHAKE:
					msg = 'HOST: %s:%s hand failed , hand msg %s' % (host,port,hand_msg)
				else:
					msg = 'HOST: %s:%s hand success!' % (host,port)
				log(msg)
			except:
			    pass

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
		log('active count: %s' % str(ac_num-1))
		if ac_num <= 1 or queue.empty():
			break

if __name__ == '__main__':
	# tasks = ['1234','5678','233333','5555','QAQAQAQ']
	tasks =[]
	ips = open('ip.txt','r').readlines()
	for ip in ips:
		host = ip.split(' ')[0]
		port = ip.split(' ')[1].split('/')[0]
		tasks.append(":".join([host,port]))
	add_task(tasks)
	socket.setdefaulttimeout(TIMEOUT)
	for i in range(0,Thread_num):
		t = ThreadNum(queue)
		t.setDaemon(True)
		t.start()
	t_join(Thread_num)

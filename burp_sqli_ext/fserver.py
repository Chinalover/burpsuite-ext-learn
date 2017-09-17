from flask import Flask
import json
from flask import request
import Queue
import threading
from isqlmap import isqlmap
import time
queue = Queue.Queue()
locker = threading.Lock()
Thread_num = 5
app = Flask(__name__)
isqlmap = isqlmap()
class ThreadNum(threading.Thread):
	"""docstring for ThreadNum"""
	def __init__(self, queue):
		threading.Thread.__init__(self)
		self.queue = queue

	def run(self):
		while True:
			try:
				if queue.empty():
					time.sleep(1)
					continue
				current_task = self.queue.get()
			except:
				time.sleep(1)
				continue
			isqlmap.extract_request(current_task[0],current_task[1],current_task[2],current_task[3])
			log(current_task[0])

def add_task(task):
	queue.put(task)
def log(info):
	locker.acquire()
	print info
	locker.release()
@app.route('/api',methods=["POST"])
def hello_world():
	uri = request.form['url']
	out = open('out_url.txt','a')
	out.write(uri+"\n")
	out.close
	#print uri
	method = request.form['method']
	#print method
	headers = json.loads(str(request.form['headers']))
	#print headers
	body = request.form['body']
	#print body
	add_task([uri,method,headers,body])
 	return 'ok'
if __name__ == '__main__':
	# tasks = ['1234','5678','233333','5555','QAQAQAQ']
	for i in range(0,Thread_num):
		t = ThreadNum(queue)
		t.setDaemon(True)
		t.start()
	app.run(port=8989)
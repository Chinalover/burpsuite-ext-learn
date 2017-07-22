"""
['__class__', '__copy__', '__deepcopy__', '__delattr__', '__doc__', '__ensure_finalizer__', '__eq__', '__format__', '__getattribute__', '__hash__', '__init__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__str__', '__subclasshook__', '__unicode__', 'class', 'comment', 'equals', 'getClass', 'getComment', 'getHighlight', 'getHost', 'getHttpService', 'getPort', 'getProtocol', 'getRequest', 'getResponse', 'getStatusCode', 'getUrl', 'hashCode', 'highlight', 'host', 'httpService', 'notify', 'notifyAll', 'port', 'protocol', 'request', 'response', 'setComment', 'setHighlight', 'setHost', 'setHttpService', 'setPort', 'setProtocol', 'setRequest', 'setResponse', 'statusCode', 'toString', 'url', 'wait']
http
['__class__', '__copy__', '__deepcopy__', '__delattr__', '__doc__', '__ensure_finalizer__', '__eq__', '__format__', '__getattribute__', '__hash__', '__init__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__str__', '__subclasshook__', '__unicode__', 'bodyOffset', 'class', 'cookies', 'equals', 'getBodyOffset', 'getClass', 'getCookies', 'getHeaders', 'getInferredMimeType', 'getStatedMimeType', 'getStatusCode', 'hashCode', 'headers', 'inferredMimeType', 'notify', 'notifyAll', 'statedMimeType', 'statusCode', 'toString', 'wait']

"""

def send_to_api(url,method,headers,body):
	import urllib,urllib2,json
	add_task_url = "http://127.0.0.1:8989/api"
	paras = {'url':url,'method':method,'headers':headers,'body':body}
	data = urllib.urlencode(paras)
	req=urllib2.Request(add_task_url, data)
	sqlreq = urllib2.urlopen(req).read()
	print sqlreq
#send_to_api('just a test')
if (messageIsRequest==1):
	a=messageInfo.getRequest()
	#print dir(messageInfo)
	# print messageInfo.protocol
	newres=helpers.analyzeResponse(a)
	url = str(messageInfo.url)
	# print messageInfo.url
	req_headers = newres.headers
	method = "POST"
	if req_headers[0][0] == "G":
		method = "GET"
	send_headers = {}
	for i in range(1,len(req_headers)):
		opt,val = req_headers[i].split(': ',1)
		send_headers[opt] = val
	import json
	send_headers = json.dumps(send_headers)
	offset=newres.getBodyOffset()
	body=a[offset:]
	body_string=body.tostring()
	print url,method,send_headers,body_string
	send_to_api(url,method,send_headers,body_string)
		# print opt,val
	# print current_ua
	# print current_cookie
	#send_to_api(url,)
	# print newres.getCookies()
	#print dir(newres)
	#print newres
	#send_to_api(messageInfo.protocol,messageInfo.port,a.tostring())

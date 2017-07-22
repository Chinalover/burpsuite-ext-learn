from flask import Flask
import json
from flask import request
app = Flask(__name__)

@app.route('/api',methods=["POST"])
def hello_world():
	from isqlmap import isqlmap
	isqlmap = isqlmap()
	uri = request.form['url']
	print uri
	method = request.form['method']
	print method
	headers = json.loads(str(request.form['headers']))
	print headers
	body = request.form['body']
	print body
	isqlmap.extract_request(uri,method,headers,body)
 	return 'ok'

if __name__ == '__main__':
    app.run(port=8989)
from flask import Flask, request, render_template
from app import app
import json


@app.route('/', methods=['GET'])
def index():
	return render_template('index.html')

@app.route('/respond', methods=['POST'])
def respond():
	data = json.loads(request.data)
	response = data.get('response')

	# Process the response
	return json.dumps({'status': 'OK', 'response': response})

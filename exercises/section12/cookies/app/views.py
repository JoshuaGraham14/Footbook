from flask import render_template, request, make_response
from app import app

@app.route('/')
def index():
   return render_template('cookie.html',title="Cookies example")

@app.route('/setcookie', methods = ['POST', 'GET'])
def setcookie():
	if request.method == 'POST':
		value = request.form['value']

	resp = make_response(render_template('cookie.html'))
	resp.set_cookie('variable_name', value)

	return resp

@app.route('/getcookie')
def getcookie():
   name = request.cookies.get('variable_name')
   return '<h1>Cookie value set to: '+name+'</h1>'

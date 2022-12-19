from flask import render_template, flash, session, url_for,request,redirect
from app import app
from .forms import SessionForm

@app.route('/')
def index():
	if 'variable' in session:
		variable = session['variable']
		return 'Variable set : ' + variable + '<br><b><a href = \'/unsetvariable\'>click here to unset variable</a></b>'
	return "Variable is not set <br><a href = '/setvariable'></b>click here to set variable</b></a>"


@app.route('/setvariable', methods = ['GET', 'POST'])
def login():
	form = SessionForm()
	if form.validate_on_submit():
		session['variable'] = form.value.data
		return redirect(url_for('index'))
	return render_template('session.html',
                           title='Session',
                           form=form)

@app.route('/unsetvariable')
def logout():
	session.pop('variable', None)
	return redirect(url_for('index'))

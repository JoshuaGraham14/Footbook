from flask import render_template, flash
from app import app
from .forms import CalculatorForm

@app.route('/', methods=['GET', 'POST'])
def home():
	home={'description':'Welcome to this application. Please select calculator to calculate two numbers.'}
	return render_template('home.html',
						   title='Home',home=home)
@app.route('/calculator', methods=['GET', 'POST'])
def calculator():
    form = CalculatorForm()
    if form.validate_on_submit():
        flash('Succesfully received form data. %s + %s  = %s'%(form.number1.data, form.number2.data, form.number1.data+form.number2.data))
    return render_template('calculator.html',
                           title='Calculator',
                           form=form)

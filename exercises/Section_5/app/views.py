from flask import render_template, flash
from app import app

@app.route('/')
def index():
    user = {'name': 'Sam Wilson'}
    return render_template('index.html',
                           user=user)

@app.route('/fruit')
def displayFruit():
    fruits = ["Apple", "Banana", "Orange", "Kiwi"]
    return render_template("fruit.html",fruits=fruits)

@app.route('/fruitWithInheritance')
def displayFruitWithInheritance():
    fruits = ["Apple", "Banana", "Orange", "Kiwi"]
    return render_template("fruit_with_inheritance.html",fruits=fruits)






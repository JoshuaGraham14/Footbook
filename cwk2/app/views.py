from flask import render_template, flash, redirect, url_for, request
from app import app, db, models
import datetime
from .forms import CreateAssessmentForm
from flask_login import login_user, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User

@app.route('/', methods=['GET', 'POST'])
def home():
    #clearDatabase() #<--Code to clear database (keep commented)
    
    #Retrieve all assessments from the database
    assessments = models.Assessment.query.all() 
    return render_template('home.html', assessments=assessments)

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    # login code goes here
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('login')) # if the user doesn't exist or password is wrong, reload the page

    login_user(user, remember=remember)
    # if the above check passes, then we know the user has the right credentials
    return redirect(url_for('profile'))

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup_post():
    # code to validate and add user to database goes here
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect(url_for('signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('signup'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/createAssessment', methods=['GET', 'POST'])
def createAssessment():
    form = CreateAssessmentForm() #create the CreateAssessment form
    if form.validate_on_submit(): #IF the form was submitted successfully:
        #Upload the data from the form to the database
        p = models.Assessment(title=form.title.data,module_code=form.module_code.data,deadline=form.deadline.data,description=form.description.data,status=False)
        #Add and commit the data
        db.session.add(p) 
        db.session.commit()
        flash('Succesfully created new assessment') #Display a success message
        return redirect(url_for('home')) #Redirect the user to the homepage

    #ELSE render the createAssessment.html template
    return render_template('createAssessment.html',
                            title='CreateAssessment',
                            form=form)

@app.route('/completedAssessments', methods=['GET', 'POST'])
def completedAssessments():
    #Retrieve all assessments from the database where the 'status' column has been set to True, i.e. assessment was completed
    assessments = models.Assessment.query.filter_by(status=True).all()
    #Render the completedAssessments.html template
    return render_template('completedAssessments.html', assessments=assessments)

@app.route('/uncompleteAssessments', methods=['GET', 'POST'])
def uncompleteAssessments():
    #Retrieve all assessments from the database where the 'status' column has been set to False, i.e. assessment is uncomplete
    assessments = models.Assessment.query.filter_by(status=False).all()
    
    if request.method == 'POST': #If a POST request has been sent, i.e. a 'Mark as Completed' button has been pressed:
        key = list(request.form.keys())[0] #retrieve the key from the request Dict (the ID of the button which was clicked)
        a = models.Assessment.query.get(int(key)) #Query this ID
        a.status = True #Set the status of this column to be True
        db.session.commit() #Commit changes

        #Again, retrieve all assessments from the database where the 'status' column has been set to False
        assessments = models.Assessment.query.filter_by(status=False).all()
        if(not assessments): #IF no uncompleted assessments were found, redirect to home page:
            return redirect(url_for('home'))
        else: #ELSE refresh the uncompleteAssessments page:
            return redirect(url_for('uncompleteAssessments'))

    #Render the uncompleteAssessments.html template
    return render_template('uncompleteAssessments.html', assessments=assessments)

#Function to clear the contents of the Assessment database
def clearDatabase():
    models.Assessment.query.delete()
    db.session.commit()
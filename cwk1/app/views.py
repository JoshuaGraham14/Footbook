from flask import render_template, flash, redirect, url_for, request
from app import app, db, models
import datetime
from .forms import CreateAssessmentForm

@app.route('/', methods=['GET', 'POST'])
def home():
    #clearDatabase() #<--Code to clear database (keep commented)
    
    #Retrieve all assessments from the database
    assessments = models.Assessment.query.all() 
    return render_template('home.html', assessments=assessments)

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
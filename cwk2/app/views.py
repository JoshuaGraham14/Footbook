from flask import render_template, flash, redirect, url_for, request
from app import app, db, admin, models
import datetime
from .forms import CreatePostForm
from flask_login import login_user, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_admin.contrib.sqla import ModelView
import json

admin.add_view(ModelView(models.User, db.session))
admin.add_view(ModelView(models.Post, db.session))

teams=["Arsenal", "Aston Villa", "Bournemouth", "Brentford", "Brighton & Hove Albion", "Chelsea", "Crystal Palace",
"Everton", "Fulham", "Leeds United", "Leicester City", "Liverpool", "Manchester City", "Manchester United",
"Newcastle United", "Nottingham Forest", "Southampton", "Tottenham Hotspur", "West Ham United", "Wolverhampton Wanderers"]

@app.route('/', methods=['GET', 'POST'])
@login_required
def home():
    #clearDatabase() #<--Code to clear database (keep commented)

    if request.method == 'POST':
        print("Filter!!!")
    
    #Retrieve all posts from the database
    posts = models.Post.query.all()
    friends_posts = []
    for post in posts:
        if(current_user in post.user.friends or current_user == post.user):
            friends_posts.append(post)
            print(post)
        for like in post.likes:
            print(like)

    print("likes", current_user.liked)
    print("dislikes", current_user.disliked)
    
    return render_template('home.html', posts=friends_posts, likedHistory=current_user.liked, dislikedHistory=current_user.disliked)

@app.route("/filter", methods=["POST"])
def filter():
    if request.method == 'POST':
        print("FILTEREDDDDDDDDDDD!!!")
        
    return "a"

@app.route("/like", methods=["POST"])
def like():
    code=""
    if request.method == 'POST': #If a POST request has been sent, i.e. a 'Mark as Completed' button has been pressed:
        like_id = request.headers["Id"]
        print("like_id", like_id)

    current_post = models.Post.query.get(like_id)
    if (current_user not in [i for i in current_post.likes]):
        current_post.likes.append(current_user)
        print("current_post.likes", current_post.likes)
        code="a"
        if (current_user in [i for i in current_post.dislikes]):
            current_post.dislikes.remove(current_user)
            numOfDislikes = len(current_post.dislikes)
            print("numOfDislikes", numOfDislikes)
            code="s"+str(numOfDislikes)
    else:
        current_post.likes.remove(current_user)
        print("current_post.likes", current_post.likes)
        code="r"

    numOfLikes = len(current_post.likes)

    db.session.commit()
    return str(numOfLikes)+code

@app.route("/dislike", methods=["POST"])
def dislike():
    code=""
    if request.method == 'POST': #If a POST request has been sent, i.e. a 'Mark as Completed' button has been pressed:
        dislike_id = request.headers["Id"]
        print("dislike_id", dislike_id)

    current_post = models.Post.query.get(dislike_id)
    if (current_user not in [i for i in current_post.dislikes]):
        current_post.dislikes.append(current_user)
        print("current_post.dislikes", current_post.dislikes)
        code="a"
        if (current_user in [i for i in current_post.likes]):
            current_post.likes.remove(current_user)
            numOfLikes = len(current_post.likes)
            print("numOfLikes", numOfLikes)
            code="s"+str(numOfLikes)
    else:
        current_post.dislikes.remove(current_user)
        print("current_post.dislikes", current_post.dislikes)
        code="r"
    
    numOfDislikes = len(current_post.dislikes)

    db.session.commit()
    return str(numOfDislikes)+code

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        logout_user()
        return redirect(url_for('home'))
    return render_template('profile.html', username=current_user.username)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    # login code goes here
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = models.User.query.filter_by(email=email).first()

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
    return render_template('signup.html', teamNames=teams)

@app.route('/signup', methods=['POST'])
def signup_post():
    # code to validate and add user to database goes here
    email = request.form.get('email')
    username = request.form.get('username')
    teamNum = int(request.form.get('team'))
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = models.User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database
    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect(url_for('signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = models.User(email=email, username=username, password=generate_password_hash(password, method='sha256'), team=teams[teamNum])

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    login_user(new_user)
    return redirect(url_for('home'))

@app.route('/createPost', methods=['GET', 'POST'])
def createPost():
    form = CreatePostForm() #create the CreatePost form
    if form.validate_on_submit(): #IF the form was submitted successfully:
        #Upload the data from the form to the database
        p = models.Post(title=form.title.data,description=form.description.data,user_id=current_user.id)
        #Add and commit the data
        db.session.add(p) 
        db.session.commit()
        flash('Succesfully created new post') #Display a success message
        return redirect(url_for('home')) #Redirect the user to the homepage

    #ELSE render the createPost.html template
    return render_template('createPost.html',
                            title='createPost',
                            form=form)

@app.route('/friends', methods=['GET', 'POST'])
def friends():
    #Retrieve all users from the database
    friends = current_user.friends
    users = models.User.query.filter((models.User.id != current_user.id)).all()
    users2 = []
    for i in friends:
        users2.append(i)
    final_users = list(set(users) - set(users2))
    
    if request.method == 'POST': #If a POST request has been sent, i.e. a 'Mark as Completed' button has been pressed:
        key = list(request.form.keys())[0] #retrieve the key from the request Dict (the ID of the button which was clicked)
        friendAdded = models.User.query.get(int(key)) #Query this ID

        current_user.friends.append(friendAdded)
        friendAdded.friends.append(current_user)

        # p = models.Friends()
        # db.session.add(p)
        # # a.status = True #Set the status of this column to be True
        db.session.commit() #Commit changes

        # #Again, retrieve all posts from the database where the 'status' column has been set to False
        # friends = models.Friends.query.all()
        # print(friends)
        # if(not assessments): #IF no uncompleted assessments were found, redirect to home page:
        #     return redirect(url_for('home'))
        # else: #ELSE refresh the uncompleteAssessments page:
        flash('Succesfully added new friend') #Display a success message
        return redirect(url_for('friends'))

    #Render the uncompleteAssessments.html template
    return render_template('friends.html', friends=friends, users=final_users)

#Function to clear the contents of the Assessment database
def clearDatabase():
    models.Post.query.delete()
    models.User.query.delete()
    db.session.commit()
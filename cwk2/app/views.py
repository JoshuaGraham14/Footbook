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
filterSelection=0
filterSelectionText="Filter by"

@app.route('/', methods=['GET', 'POST'])
@login_required
def home():
    #clearDatabase() #<--Code to clear database (keep commented)
    global filterSelection
    global filterSelectionText

    print("filterSelection:",filterSelection, " filterSelectionText:",filterSelectionText)

    posts = models.Post.query.all()
    if(filterSelection==1):
        # filterSelectionText = "All "
        posts = models.Post.query.all()
    elif(filterSelection==2):
        posts = models.Post.query.all()
        friends = current_user.friends
        friends_posts = []
        for post in posts:
            if(current_user in post.user.friends):
                friends_posts.append(post)
        posts=friends_posts
    elif(filterSelection==3):
        posts = models.Post.query.all()
        team_posts = []
        for post in posts:
            if(current_user.team in post.user.team):
                team_posts.append(post)
        posts=team_posts

    print("posts:", posts)
    print("likes", current_user.liked)
    print("dislikes", current_user.disliked)
    print(posts, current_user.liked, current_user.disliked, filterSelection)
    for post in posts:
        print(post.user)
    
    print("HOME LOADEDDDDD 22222")
    return render_template('home.html', posts=posts, current_user=current_user, filterSelectionText=filterSelectionText)

@app.route("/filter", methods=["POST"])
def filter():
    global filterSelection
    global filterSelectionText
    
    if request.method == 'POST':
        print("FILTEREDDDDDDDDDDD!!!")
        selection_id = request.headers["Id"]
        if(selection_id=="1"):
            filterSelection=1
            filterSelectionText="All "
        elif(selection_id=="2"):
            filterSelection=2
            filterSelectionText="My Friends Only "
        else:
            filterSelection=3
            filterSelectionText="My Team Only "
        return redirect(url_for('home'))

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
        global filterSelection
        global filterSelectionText
        filterSelection=0
        filterSelectionText="Filter by"
        return redirect(url_for('home'))
    
    posts = models.Post.query.filter_by(user=current_user)

    return render_template('profile.html', username=current_user.username, posts=posts, likedHistory=current_user.liked, dislikedHistory=current_user.disliked)

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
    return redirect(url_for('home'))

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
        code=key[0]
        user_id=key[1:]
        if(code == "r"):
            friendRemoved = models.User.query.get(int(user_id)) #Query this ID
            print("friendRemoved:",friendRemoved)
            current_user.friends.remove(friendRemoved)
            friendRemoved.friends.remove(current_user)
            flash('Succesfully removed friend') #Display a success message
        elif(code == "a"):
            friendAdded = models.User.query.get(int(user_id)) #Query this ID
            print("friendAdded:",friendAdded)
            current_user.friends.append(friendAdded)
            friendAdded.friends.append(current_user)
            flash('Succesfully added new friend') #Display a success message

        db.session.commit() #Commit changes

        return redirect(url_for('friends'))

    #Render the uncompleteAssessments.html template
    return render_template('friends.html', friends=friends, users=final_users)

#Function to clear the contents of the Assessment database
def clearDatabase():
    models.Post.query.delete()
    models.User.query.delete()
    db.session.commit()
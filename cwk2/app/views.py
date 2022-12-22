from flask import render_template, flash, redirect, url_for, request
from app import app, db, admin, models
from datetime import datetime
from .forms import CreatePostForm, LoginForm, SignupForm, ChangePasswordForm ,teams
from flask_login import login_user, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_admin.contrib.sqla import ModelView
import json
import logging

admin.add_view(ModelView(models.User, db.session))
admin.add_view(ModelView(models.Post, db.session))

app.logger.info('index route request')

filterSelection=0
filterSelectionText="Filter by"

@app.route('/', methods=['GET', 'POST'])
def home():
    #clearDatabase() #<--Code to clear database (keep commented)
    app.logger.info('Home Page')
    global filterSelection
    global filterSelectionText
    
    posts = models.Post.query.order_by(models.Post.dateTimePosted.desc()).all()
    if not current_user.is_anonymous:
        if(filterSelection==1):
            posts = models.Post.query.order_by(models.Post.dateTimePosted.desc()).all()
        elif(filterSelection==2):
            posts = models.Post.query.all()
            friends = current_user.friends
            friends_posts = []
            for post in posts:
                if(current_user in post.user.friends):
                    friends_posts.append(post)
            posts=friends_posts
            posts.reverse()

        elif(filterSelection==3):
            posts = models.Post.query.all()
            team_posts = []
            for post in posts:
                if(current_user.team in post.user.team):
                    team_posts.append(post)
            posts=team_posts
            posts.reverse()
        app.logger.info('selected filter: "%s"', filterSelectionText)
    
    return render_template('home.html', posts=posts, current_user=current_user, filterSelectionText=filterSelectionText)
    

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        key = list(request.form.keys())[0]
        if(key == "l"):
            app.logger.info('User logged out')
            logout_user()
            global filterSelection
            global filterSelectionText
            filterSelection=0
            filterSelectionText="Filter by"
            return redirect(url_for('home'))
        else:
            return redirect(url_for('changePassword'))
    
    posts = models.Post.query.filter_by(user=current_user).order_by(models.Post.dateTimePosted.desc()).limit(10)

    return render_template('profile.html', username=current_user.username, posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm() #create the Login form
    if form.validate_on_submit(): #IF the form was submitted successfully:
        email=form.email.data
        password = form.password.data
        remember = form.remember.data

        user = models.User.query.filter_by(email=email).first()
        # take the user-supplied password, hash it, and compare it to the hashed password in the database
        if not user or not check_password_hash(user.password, password):
            flash('Please check your login details and try again.')
            app.logger.warning('Login details incorrect')
            return redirect(url_for('login')) # if the password is wrong, reload the page

        # if the above check passes, then we know the user has the right credentials
        login_user(user, remember=remember)
        app.logger.info('%s logged in successfully', user.username)
        flash('Logged in successfully')
        return redirect(url_for('home'))

    return render_template('login.html', title='login', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm() #create the SignupForm form
    if form.validate_on_submit(): #IF the form was submitted successfully:
        email=form.email.data
        username=form.username.data
        team=teams[int(form.team.data)]
        password = form.password.data

        user = models.User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database
        if user: # if a user is found, we want to redirect back to signup page so user can try again
            flash('Email address already exists')
            app.logger.warning('Email address already exists: %s', email)
            return redirect(url_for('signup'))

        user = models.User.query.filter_by(username=username).first() # if this returns a user, then the username already exists in database
        if user: # if a user is found, we want to redirect back to signup page so user can try again
            flash('Username already exists')
            app.logger.warning('Username already exists: %s', username)
            return redirect(url_for('signup'))

        # if the above check passes, then we know the user has the right credentials

        # create a new user with the form data. Hash the password so the plaintext version isn't saved.
        new_user = models.User(email=email, username=username, password=generate_password_hash(password, method='sha256'), team=team)
        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()
        
        login_user(new_user)
        app.logger.info('%s signed up successfully', username)
        flash('Signed up successfully. This site uses cookies.')
        return redirect(url_for('home'))        
    return render_template('signup.html', title='signup', form=form)

@app.route('/createPost', methods=['GET', 'POST'])
@login_required
def createPost():
    form = CreatePostForm() #create the CreatePost form
    if form.validate_on_submit(): #IF the form was submitted successfully:
        p = models.Post(title=form.title.data,description=form.description.data,dateTimePosted=datetime.now(),user_id=current_user.id)
        #Add and commit the data
        db.session.add(p) 
        db.session.commit()
        flash('Succesfully created new post') #Display a success message
        app.logger.info('Created new post')
        return redirect(url_for('home')) #Redirect the user to the homepage

    #ELSE render the createPost.html template
    return render_template('createPost.html', title='createPost', form=form)

@app.route('/friends', methods=['GET', 'POST'])
@login_required
def friends():
    friends = current_user.friends
    users = models.User.query.filter((models.User.id != current_user.id)).all()
    users2 = []
    for i in friends:
        users2.append(i)
    final_users = list(set(users) - set(users2))

    if request.method == 'POST': #If a POST request has been sent, i.e. a 'Add Friend'/'Remove Friend' button has been pressed:
        key = list(request.form.keys())[0] #retrieve the key from the request Dict (the ID of the button which was clicked)
        code=key[0]
        user_id=key[1:]
        if(code == "r"):
            friendRemoved = models.User.query.get(int(user_id)) #Query this ID
            app.logger.info('Friend removed: %s', friendRemoved)
            current_user.friends.remove(friendRemoved)
            friendRemoved.friends.remove(current_user)
            flash('Succesfully removed friend') #Display a success message
        elif(code == "a"):
            friendAdded = models.User.query.get(int(user_id)) #Query this ID
            app.logger.info('Friend added: %s', friendAdded)
            current_user.friends.append(friendAdded)
            friendAdded.friends.append(current_user)
            flash('Succesfully added new friend') #Display a success message

        db.session.commit() #Commit changes
        return redirect(url_for('friends'))

    #Render the friends.html template
    return render_template('friends.html', friends=friends, users=final_users)

@app.route('/viewProfile/<username>', methods=['GET', 'POST'])
def viewProfile(username):
    if request.method == 'POST':
        key = list(request.form.keys())[0] #retrieve the key from the request Dict (the ID of the button which was clicked)
        code=key[0]
        user_id=key[1:]
        if(code == "r"):
            friendRemoved = models.User.query.get(int(user_id)) #Query this ID
            app.logger.info('Friend removed: %s', friendRemoved)
            current_user.friends.remove(friendRemoved)
            friendRemoved.friends.remove(current_user)
            flash('Succesfully removed friend') #Display a success message
        elif(code == "a"):
            friendAdded = models.User.query.get(int(user_id)) #Query this ID
            app.logger.info('Friend added: %s', friendAdded)
            current_user.friends.append(friendAdded)
            friendAdded.friends.append(current_user)
            flash('Succesfully added new friend') #Display a success message

        db.session.commit() #Commit changes
        return redirect(url_for('viewProfile', username=username))

    app.logger.info('Viewing %s\'s profile', username)
    user = models.User.query.filter(models.User.username == username).first()
    posts = models.Post.query.filter_by(user=user).order_by(models.Post.dateTimePosted.desc()).limit(10)
    isFriend = current_user in user.friends
    return render_template('viewProfile.html', user=user, posts=posts, isFriend=isFriend)

@app.route('/changePassword', methods=['GET', 'POST'])
def changePassword():
    form = ChangePasswordForm() #create the ChangePasswordForm form
    if form.validate_on_submit(): #IF the form was submitted successfully:
        oldPassword = form.oldPassword.data
        newPassword = form.newPassword.data

        if not check_password_hash(current_user.password, oldPassword):
            flash('Incorrect password. Try again.')
            app.logger.warning('Incorrect password')
            return redirect(url_for('changePassword')) # if the password is wrong, reload the page
        
        if oldPassword==newPassword:
            flash('Cannot reuse the same password. Try again.')
            app.logger.warning('Cannot reuse the same password')
            return redirect(url_for('changePassword')) # if the password is reused, reload the page

        # if the above check passes, then we know the user has the right credentials

        # update the password with the form data. Hash the password so the plaintext version isn't saved.
        current_user.password = generate_password_hash(newPassword, method='sha256')
        db.session.commit()

        app.logger.info('%s password updated successfully', current_user.username)
        flash('Password updated successfully.')
        return redirect(url_for('home'))

    return render_template('changePassword.html', title='changePassword', form=form)

@app.route("/filter", methods=["POST"])
def filter():
    global filterSelection
    global filterSelectionText
    
    if request.method == 'POST':
        app.logger.info('Filter Selected')
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
    if request.method == 'POST':
        like_id = request.headers["Id"]

    current_post = models.Post.query.get(like_id)
    app.logger.info('Post (%s) Was Liked', current_post.id)
    if (current_user not in [i for i in current_post.likes]):
        current_post.likes.append(current_user)
        code="a"
        if (current_user in [i for i in current_post.dislikes]):
            current_post.dislikes.remove(current_user)
            numOfDislikes = len(current_post.dislikes)
            code="s"+str(numOfDislikes)
    else:
        current_post.likes.remove(current_user)
        code="r"

    numOfLikes = len(current_post.likes)

    db.session.commit()
    return str(numOfLikes)+code

@app.route("/dislike", methods=["POST"])
def dislike():
    code=""
    if request.method == 'POST':
        dislike_id = request.headers["Id"]

    current_post = models.Post.query.get(dislike_id)
    app.logger.info('Post (%s) Was Disliked', current_post.id)
    if (current_user not in [i for i in current_post.dislikes]):
        current_post.dislikes.append(current_user)
        code="a"
        if (current_user in [i for i in current_post.likes]):
            current_post.likes.remove(current_user)
            numOfLikes = len(current_post.likes)
            code="s"+str(numOfLikes)
    else:
        current_post.dislikes.remove(current_user)
        code="r"
    
    numOfDislikes = len(current_post.dislikes)

    db.session.commit()
    return str(numOfDislikes)+code

#Function to clear the contents of the Assessment database
def clearDatabase():
    models.Post.query.delete()
    models.User.query.delete()
    db.session.commit()
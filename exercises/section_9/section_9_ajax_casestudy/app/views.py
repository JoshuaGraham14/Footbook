from app import app, models, db
from flask import render_template, flash, request
from .forms import IdeaForm
import json


@app.route('/', methods=['GET', 'POST'])
def index():

	form = IdeaForm()
	if form.validate_on_submit():
		# Save idea
		new_idea = models.Idea(text=form.idea.data)
		db.session.add(new_idea)
		db.session.commit()

		flash("Thanks for your bright new idea: " + str(form.idea.data))

	# Query after having added new idea
	ideas = models.Idea.query.all()
	print("Number of ideas in db:", len(ideas))

	return render_template('index.html', form=form, ideas=ideas)

# @csrf.exempt
@app.route('/vote', methods=['POST'])
def vote():
	data = json.loads(request.data)
	idea_id = int(data.get('idea_id'))
	idea = models.Idea.query.get(idea_id)

	if data.get('vote_type') == "up":
		idea.upvotes += 1
	else:
		idea.downvotes += 1

	db.session.commit()
	return json.dumps({'status':'OK','upvotes': idea.upvotes, 'downvotes': idea.downvotes })

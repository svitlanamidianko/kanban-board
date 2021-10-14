# by S Midianko
# spring 2021
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# defining the app itself
app = Flask(__name__)

# setting up an address for the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///kanban.db'
db = SQLAlchemy(app)

# this is a composite index table for many-to-many relationship that i have. 
# specifically, one task can have many tags, and one tag can be related to many tasks. 
# this table is automatically filled, given that I defined *relationship* in other two tables.
tags = db.Table('tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
    db.Column('task_id', db.Integer, db.ForeignKey('task.id'), primary_key=True)
)

# main table for the tasks. It inherits main functionality from db.Model. 
class Task(db.Model): 
    id = db.Column(db.Integer, primary_key = True) # unique id that it automatically generated.
    name = db.Column(db.String(50)) # self-explanatory
    description = db.Column(db.String(350)) # self-explanatory
    category = db.Column(db.String(20)) # can be 'wip' 'done' 'todo' or 'deleted'
    # relationship necessary for the composite index table above.
    tags = db.relationship('Tag', secondary=tags, lazy='subquery',
        backref=db.backref('pages', lazy=True))
# tags table
class Tag(db.Model):
    id = db.Column(db.Integer, primary_key = True, unique=True)
    name = db.Column(db.String(20), unique=True) 

# defining tags at the beginning and putting them in.
tag1 = Tag( name='hobby')
tag2 = Tag( name='chores')
tag3 = Tag( name='minerva')
tag4 = Tag( name='important')
tag5 = Tag( name='non-important')
tag6 = Tag( name='non-urgent')
tag7 = Tag( name='urgent')

# we will only add those tags if they are not in db right now. The case when they are in db 
# happens when we running python3 kanbanapp.py file from the terminal twice, without deleting
# the values in the database. 
for i in [tag1,tag2, tag3, tag4, tag5, tag6, tag7]: 
    exists = Tag.query.filter_by(name = i.name).first()
    if not exists:
        db.session.add(i)
db.session.commit()

# defining the route with main index rendering.
@app.route('/')
def index():
    # we will query all the tasks by the category and pass those
    # queries as a parameter to the render_template. 
    # these input values wll them be used to fill the html up with content.
    todos = Task.query.filter_by(category = "todo").all()
    dones = Task.query.filter_by(category = "done").all()
    wips = Task.query.filter_by(category = "wip").all()
    tags = Tag.query.all()    
    return render_template('index.html', todos = todos, dones = dones, wips = wips, tags=tags)

# below are different routes for "add the card" functionality.
@app.route('/addtodo', methods = ['POST']) #creating route
def addtodo(): 
    # creating a row in task db with values iputted by the users
    todo = Task(name = request.form['taskname'], description = request.form['taskdescription'], category = "todo" ) #
    # also appending 'children' of the row, which will be added into the composite joned tables of 
    # tags. 
    for tag_ in request.form.getlist('tags'): 
        todo.tags.append(Tag.query.filter_by(name = tag_).first())
    db.session.add(todo)
    db.session.commit()
    return redirect(url_for('index'))

# same as above, but for Work in progress task
@app.route('/addwip', methods = ['POST']) #creating route
def addwip(): 
    todo = Task(name = request.form['taskname2'], description = request.form['taskdescription2'], category = "wip" ) # save to DB
    for tag_ in request.form.getlist('tags'): 
        todo.tags.append(Tag.query.filter_by(name = tag_).first())
    db.session.add(todo)
    db.session.commit()
    return redirect(url_for('index'))

# same as above, but for done task.
@app.route('/adddone', methods = ['POST']) #creating route
def adddone(): 
    todo = Task(name = request.form['taskname3'], description = request.form['taskdescription3'], category = "done" ) # save to DB
    for tag_ in request.form.getlist('tags'): 
        todo.tags.append(Tag.query.filter_by(name = tag_).first())
    db.session.add(todo)
    db.session.commit()
    return redirect(url_for('index'))

# this is function for updating cards and 'moving them' between the categories. 
# depending on what button was clicked, the category of the task will be changed. 
@app.route('/updatedone', methods = ['POST']) #creating route
def updatedone(): 
    # the value submitted in the button is in a form of dictionary. 
    # we will iterate over it.
    dict_submitted = request.form
    for key, val in dict_submitted.items():
        todo = Task.query.get(key)
        if val == 'mark as done':
            todo.category = 'done'
        elif val == 'mark as wip':
            todo.category = 'wip'
        elif val == 'mark as todo':
            todo.category = 'todo'
        else: 
            todo.category = 'deleted'
    db.session.commit()
    return redirect(url_for('index'))
    
# running the app.
if __name__ =='__main__': 
    app.run(debug = True)
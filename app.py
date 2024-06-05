import json
import datetime
from forms import CourseForm
from flask import (Flask, abort, render_template, 
                   request, url_for, flash, redirect)
from flask_wtf import CSRFProtect


# Initialize Flask Object
app = Flask(__name__)

# Secret Key
app.config['SECRET_KEY'] = b'\xecG\x0e\x82\x06<\xe6\x99}q\x95z\x81\xc2\xf8\xc4O\r\xd3\xc8\x98\xec\x12\xd3\x89\x9al'
# CSRFProtect().init_app(app)

##############################
# Storage Handling Functions #
##############################

def load_course_list():
  """Loads the course list from a JSON file."""
  try:
    with open('courses.json', 'r') as f:
      return json.load(f)
  except FileNotFoundError:
    return []  # Return an empty list if the file doesn't exist

def save_course_list(courses):
  """Saves the course list to a JSON file."""
  with open('courses.json', 'w') as f:
    json.dump(courses, f, indent=4)  # Add indentation for readability

def load_message_list():
  """Loads the message list from a JSON file."""
  try:
    with open('messages.json', 'r') as f:
      return json.load(f)
  except FileNotFoundError:
    return []  # Return an empty list if the file doesn't exist

def save_message_list(messages):
  """Saves the message list to a JSON file."""
  with open('messages.json', 'w') as f:
    json.dump(messages, f, indent=4)  # Add indentation for readability


##############################
###### Main Page Routes ######
##############################

@app.route('/')
def hello():
    '''
    Renders ./templates/index.html 
    Current UTC is passed to render file.
    '''
    return render_template('index.html', current_time=datetime.datetime.utcnow())

@app.route('/about')
def about():
    '''
    Renders ./templates/about.html 
    '''
    return render_template('about.html')

@app.route('/messages')
def messages():
    '''
    Renders ./templates/messages.html
    '''
    inbox=load_message_list()
    try:
        app.logger.info('Passing API and Rendering')
        return render_template('messages.html', msgs=inbox)
    except:
        app.logger.error('Internal Code Error')
        abort(500)
                           
@app.route('/comments')
def comments():
    '''
    Renders ./templates/comments.html
    Local List 'comments' is passed to render file.
    '''
    app.logger.info('Building list of comments...')
    comments = ['This is the first comment.',
                'This is the second comment.',
                'This is the third comment.',
                'This is the fourth comment.'
                ]
    try:
        app.logger.info('GET comments.html')
        return render_template('comments.html', comments=comments)
    except: 
        app.logger.error('Internal Code Error')
        abort(500)

@app.route('/courses')
def courses():
    courses = load_course_list()
    return render_template('courses.html', courses=courses)

##############################
#### Error Message Routes ####
##############################

@app.route('/magic/<int:mid>')
def magic(mid):
    '''
    Renders ./templates/magic.html 
    Entry from Local Magic hashtable is passed to render file.
    '''
    app.logger.info('Building magic hashtable...')
    magic = {
        200: "Success",
        304: "Yes Master",
        404: "You Lost Bro?",
        500: "Fix your code bruv"
    }
    try:
        app.logger.info(f'Magic ID {mid}')
        return render_template('magic.html', magic=magic[mid])
    except KeyError:
        app.logger.error(f'Message ID {mid} is not in messages hashtable')
        abort(404)

@app.errorhandler(404)
def page_not_found(error):
    '''
    Render 404.html on Webpage Not Found Error
    '''
    return render_template('404.html'), 404

@app.errorhandler(405)
def page_not_found(error):
    '''
    Render 405.html on Method Not Allowed Error
    '''
    return render_template('405.html'), 405

@app.errorhandler(500)
def internal_error(error):
    '''
    Render 500.html on Internal Code Error
    '''
    return render_template('500.html'), 500

##############################
######## Form Routes #########
##############################

@app.route('/add_message', methods=('GET', 'POST'))
def add_message():
    msgs = load_message_list()
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        if not title:  # Check for empty title
            flash('Title is required!')
        elif not content:  # Check for empty content
            flash('Content is required!')
        else:
            msgs.append({'title': title, 'content': content})
            save_message_list(msgs)
            return redirect(url_for('messages'))

    return render_template('add_message.html')

@app.route('/add_course', methods=('GET', 'POST'))
def add_course():
    app.logger.info('Reading API...')
    courses_list = load_course_list()
    form = CourseForm()
    if form.validate_on_submit():
        courses_list.append({'title': form.title.data,
                             'description': form.description.data,
                             'price': form.price.data,
                             'available': form.available.data,
                             'level': form.level.data
                             })
        app.logger.info('Writing to API...')
        save_course_list(courses_list)
        return redirect(url_for('courses'))
    return render_template('add_form.html', form=form)

##############################
###### URL Logic Routes ######
##############################

@app.route('/capitalize/<word>/')
def capitalize(word):
    '''
    A capitlized word fed from the subdirectory of URL is displayed as an HTML Heading.
    '''
    return f'<h1>{word.capitalize()}</h1>'

@app.route('/add/<int:n1>/<int:n2>/')
def add(n1, n2):
    '''
    Sum of two numbers is displayed as an HTML Heading. Numbers are received as consecutive subdirectories of a URL.
    '''
    return f'<h1>{n1 + n2}</h1>'

@app.route('/users/<int:user_id>/')
def greet_user(user_id):
    '''
    Displays Username based on Userid. Userid provided in URL subdirectory 
    '''
    app.logger.info('Building users hashtable...')
    users = {
        12:'Areeb',
        34:'Abeerah',
        45:'Rizwan'
        }
    try:
        return f'<h2>Hello, {users[user_id]}!</h2>'
    except :
        abort(404)



if __name__ == "__main__":

    app.debug = True
    app.run(port=5001)
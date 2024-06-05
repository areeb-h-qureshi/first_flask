import datetime
from flask import Flask, abort, render_template


app = Flask(__name__)

##############################
######## Page Routes #########
##############################

@app.route('/')
@app.route('/index')
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

@app.route('/comments/')
def comments():
    '''
    Renders ./templates/comments.html
    A list of text named comments is passed to render file.
    '''
    comments = ['This is the first comment.',
                'This is the second comment.',
                'This is the third comment.',
                'This is the fourth comment.'
                ]

    return render_template('comments.html', comments=comments)

##############################
#### Error Message Routes ####
##############################

@app.route('/messages/<int:idx>')
def message(idx):
    '''
    Renders ./templates/message.html 
    Entry from messages hashtable is passed to render file.
    '''
    messages = {
        200: "Success",
        304: "Yes Master",
        404: "You Lost Bro?",
        500: "Fix your code bruv"
    }
    return render_template('message.html', message=messages[idx])

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
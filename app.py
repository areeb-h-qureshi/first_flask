import datetime
from flask import Flask, abort, render_template


app = Flask(__name__)

messages = [{'title': 'Message One',
             'content': 'Message One Content'},
            {'title': 'Message Two',
             'content': 'Message Two Content'}
            ]

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
    return render_template('messages.html', messages=messages)

@app.route('/comments/')
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
        abort(404)

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
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

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
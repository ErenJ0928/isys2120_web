# Importing the Flask Framework

from modules  import *
from flask import *
import database
import configparser


page = {}
session = {}

# Initialise the FLASK application
app = Flask(__name__)
app.secret_key = 'SoMeSeCrEtKeYhErE'


# Debug = true if you want debug output on error ; change to false if you dont
app.debug = True


# Read my unikey to show me a personalised app
config = configparser.ConfigParser()
config.read('config.ini')
unikey = config['DATABASE']['user']
portchoice = config['FLASK']['port']

#####################################################
##  INDEX
#####################################################

# What happens when we go to our website
@app.route('/')
def index():
    # If the user is not logged in, then make them go to the login page
    if( 'logged_in' not in session or not session['logged_in']):
        return redirect(url_for('login'))
    page['unikey'] = unikey
    page['title'] = 'Welcome'
    return render_template('welcome.html', session=session, page=page)

################################################################################
# Login Page
################################################################################

# This is for the login
# Look at the methods [post, get] that corresponds with form actions etc.
@app.route('/login', methods=['POST', 'GET'])
def login():
    page = {'title' : 'Login', 'unikey' : unikey}
    # If it's a post method handle it nicely
    if(request.method == 'POST'):
        # Get our login value
        val = database.check_login(request.form['sid'], request.form['password'])

        # If our database connection gave back an error
        if(val == None):
            flash("""Error with the database connection. Please check your terminal
            and make sure you updated your INI files.""")
            return redirect(url_for('login'))

        # If it's null, or nothing came up, flash a message saying error
        # And make them go back to the login screen
        if(val is None or len(val) < 1):
            flash('There was an error logging you in')
            return redirect(url_for('login'))
        # If it was successful, then we can log them in :)
        session['name'] = val[1]
        session['sid'] = request.form['sid']
        session['logged_in'] = True
        return redirect(url_for('index'))
    else:
        # Else, they're just looking at the page :)
        if('logged_in' in session and session['logged_in'] == True):
            return redirect(url_for('index'))
        return render_template('index.html', page=page)


################################################################################
# Logout Endpoint
################################################################################

@app.route('/logout')
def logout():
    session['logged_in'] = False
    flash('You have been logged out')
    return redirect(url_for('index'))


################################################################################
# Transcript Page
################################################################################

@app.route('/transcript')
def transcript():
    # TODO
    # Now it's your turn to add to this ;)
    # Good luck!
    #   Look at the function below
    #   Look at database.py
    #   Look at units.html and transcript.html
    
    grades = database.get_transcript(session['sid'])
    
    
    return render_template('transcript.html', page=page, session=session,grades=grades)


################################################################################
# List Units page
################################################################################

# List the units of study
@app.route('/list-units')
def list_units():
    # Go into the database file and get the list_units() function
    units = database.list_units()
    
    # What happens if units are null?
    if (units is None):
        # Set it to an empty list and show error message
        units = []
        flash('Error, there are no units of study')
    page['title'] = 'Units of Study'
    return render_template('units.html', page=page, session=session, units=units)

################################################################################
# List Classrooms page
################################################################################

# List the classrooms 
@app.route('/list-classrooms')
def list_classrooms():

    units = database.list_classrooms()
    
    # What happens if units are null?
    if (units is None):
        # Set it to an empty list and show error message
        units = []
        flash('Error, there are no units of study')
    page['title'] = 'Classrooms'
    return render_template('classrooms.html', page=page, session=session, units=units)

################################################################################
# List Seats page
################################################################################

# List classrooms more than a number of seats

@app.route('/list-seats', methods=['POST', 'GET'])
def list_seats():
   
    # If it's a post method handle it nicely
    if(request.method == 'POST'):
        # Get our login value
        seats = request.form['seats']
        units = database.list_seats(seats)

        # If our database connection gave back an error
        if(units is None):
            units = []
            flash('Error, there are no units of study')
        page['title'] = 'Classrooms of each type'
        return render_template('seats.html', page=page, session=session, units=units)
 
    else:
        # Else, they're just looking at the page :)
        return render_template('seats.html', page=page)

################################################################################
# List each type of classrooms
################################################################################

# List the classrooms of each type
@app.route('/list-types')
def list_types():

    units = database.list_types()
    
    # What happens if units are null?
    if (units is None):
        # Set it to an empty list and show error message
        units = []
        flash('Error, there are no units of study')
    page['title'] = 'Types'
    return render_template('types.html', page=page, session=session, units=units)

################################################################################
# List insert page
################################################################################

# List insert
@app.route('/insert', methods=['POST', 'GET'])
def insert():
    units = database.list_uniclassroom()
    if(request.method == 'POST'):
        # Get our login value
        classroomid = request.form['classroomid']
        seats = request.form['seats']
        type = request.form['type']
        database.insert(classroomid, seats, type)
        
        # If our database connection gave back an error
        if(units is None):
            units = []
            flash('Error, there are no units of study')
    
        page['title'] = 'Insert information'
        return render_template('insert.html', page=page, session=session, units=units)
    
    else:
        # Else, they're just looking at the page :)
        return render_template('insert.html', page=page)
    
    
################################################################################
# List additional lecture page
################################################################################
# List the classrooms 
@app.route('/list-lecture')
def list_lecture():

    units = database.list_lecture()
    
    # What happens if units are null?
    if (units is None):
        # Set it to an empty list and show error message
        units = []
        flash('Error, there are no units of study')
    page['title'] = 'Lecture'
    return render_template('lecture.html', page=page, session=session, units=units)


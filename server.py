# prevents false linting error for request.forms.get
# pylint: disable=E1101

import bottle
import re
import database_helper
#import threading

# this class handles all page and POST requests from the web client
class Server(bottle.Bottle):

    def __init__(self, host = '127.0.0.1', port = '8080', database_file = ''):
        # initialize bottle functionality
        super().__init__()

        self.host = host
        self.port = port

        # load database file and create users table
        self.db = database_helper.DatabaseHelper(database_file)
        self.db.create_users_table()

        # establish routing
        self.bind_routes()

    # links routes on the site to member functions that return HTML
    def bind_routes(self):
        self.route('/', callback = self.root)
        self.route('<filename:re:.*\.css>', callback = self.send_css)
        self.route('<filename:re:.*\.js>', callback = self.send_js)
        self.post('/login', callback = self.check_login_info)
    
    # fire it up
    def start(self):
        self.run(debug = True, host = self.host, port = self.port)

    # sends a login page to new users
    def root(self):
        return self.send_login()

    # sends a login page, possibly with alert
    # accepts default values for login fields
    def send_login(self, alert = False, first = '', last = '', email = ''):
        data = {
            'logged_in': False,
            'alert': alert,
            'first': first,
            'last': last,
            'email': email,
        }
        return bottle.template('static/templates/index.tpl', data)

    # checks to see if posted user info passes checks
    # if so, show the homepage
    # if not, throw an alert
    def check_login_info(self):
        first = bottle.request.forms.get('first')
        last = bottle.request.forms.get('last')
        email = bottle.request.forms.get('email')

        # if any input is null
        if (first.strip() is None) or (last.strip() is None) or (email.strip() is None):
            return self.send_login("Input cannot be empty!", first, last, email)

        # if email is improperly formatted
        if not self.check_email_format(email):
            return self.send_login("Improperly formatted email address!", first, last, email)
        
        # if user already exists
        if self.db.query("SELECT * FROM users WHERE email = ?", email):
            return self.send_login("User already exists!", first, last, email)
        
        # if all checks have passed, add them to the database
        else:
            self.db.insert("INSERT INTO users (first, last, email) VALUES (?, ?, ?)", first, last, email)
            return self.send_homepage(first, last, email)

    # display current users' info along with info of users in database
    def send_homepage(self, first, last, email):
        data = {
            'logged_in': True,
            'alert': False,
            'first': first,
            'last': last,
            'email': email,
            'other_users': self.db.query("SELECT first, last, email FROM users WHERE email != ?", email)
        }
        return bottle.template('static/templates/index.tpl', data)

    # for serving css
    def send_css(self, filename):
        return bottle.static_file(filename, root = 'static/css')

    # for running scripts
    def send_js(self, filename):
        return bottle.static_file(filename, root = 'static/js')

    # checks for the format [1+ characters]@[1+ characters].[2+ lowercase letters]
    # returns True is format is matched, False otherwise
    def check_email_format(self, email):
        return re.search(r'.+@.+\.[a-z]{2,}', email) is not None

if __name__ == "__main__":
    server = Server(database_file = 'data/users.db')
    server.start()

    # proof that multiple instances can run simultaneously without conflicting with each other, which means 
    # the Server class is portable and self-contained
    #threading.Thread(target = lambda: Server(port = '8080', database_file = 'data/users.db').start()).start()
    #threading.Thread(target = lambda: Server(port = '8081', database_file = ':memory:').start()).start()
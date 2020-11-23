from flask import Flask, jsonify, g
from flask_cors import CORS
from resources.items import item
from resources.users import users
import models
from flask_login import LoginManager

DEBUG = True
PORT = 8000

app = Flask(__name__)

app.secret_key = "This is the secret key. Here it is."

login_manager = LoginManager()

login_manager.init_app(app)

app.register_blueprint(item, url_prefix='/api/v1/resources')
app.register_blueprint(users, url_prefix='/api/v1/users')


CORS(app, supports_credentials = True)

@login_manager.user_loader
def load_user(user_id):
    try:
        print("loading the following user")
        user = models.User.get_by_id(user_id)
        return user
        # should return None not raise an exception if the ID is not valid
    except models.DoesNotExist:
        return None

@app.before_request
def before_request():
    """Connect to the database before each request."""
    g.db = models.DATABASE
    g.db.connect()

@app.after_request
def after_request(response):
    """Close the database connection after each request."""
    g.db.close()
    return response

@app.route('/')
def index():
	return "Hello"

@app.route('/sayhi/<username>')
def hello(username):
	return "Hello {}".format(username)

if __name__ == "__main__":
	models.initialize()
	app.run(debug=DEBUG, port=PORT)

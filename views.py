from flask import Flask
from datetime import datetime
from flask import render_template
from flask import redirect
application = Flask(__name__)

@application.route('/')
@application.route('/home')
def home():
	return "<h1 style='color:blue'>Hello There!</h1>"

@application.errorhandler(404)
def page_not_found(e):
    """Custom 404 Page."""
    return "<h1 style='color:red'>404 Error :(</h1>", 404

@application.errorhandler(500)
def page_not_found(e):
    """Custom 500 Page."""
    return "<h1 style='color:red'>500 Error :(</h1>", 500

if __name__ == "__main__":
    application.run(host='0.0.0.0')

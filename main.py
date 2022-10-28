import os
from datetime import timedelta

from flask import Flask,session

from configurations import *
from models import db
from resources import csrf, login_manager, ckeditor
from utilities.create_fields import *

app = Flask(__name__)

# app.config.from_object(Testing)
# app.config.from_object(Production)
app.config.from_object(Development)

db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()
    seeding()

csrf.init_app(app)
ckeditor.init_app(app)
login_manager.init_app(app)

login_manager.login_view = 'login'
login_manager.login_message = u"Log in to access more resources."
login_manager.login_message_category = "info"
login_manager.refresh_view = 'login'
login_manager.needs_refresh_message = u"Session timedout, please login again"
login_manager.needs_refresh_message_category = "info"

app.app_context().push()

@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=30)


from resources.home_views import *
from resources.auth import *
from resources.employer import *
from resources.provider import *
from resources.admin import *

if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 6100, threaded=True)
    # app.run(threaded=True)
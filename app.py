from application import app
from flask import current_app as app
from application.database import db

import flask_excel as excel

with app.app_context():
    
    db.create_all()

import Add_Roles
import Add_Users
import Add_Group

app.run(host = "0.0.0.0", port=5000, debug=True)

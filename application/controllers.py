from flask import request, url_for, redirect, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from flask_security import auth_required, login_user, hash_password, roles_required
from flask import render_template
from flask import current_app as app
from werkzeug.utils import secure_filename
from application.database import db
from datetime import datetime
from datetime import timedelta
import os
from email_validator import validate_email
from application.models import *


@app.route("/")
def index():
    return render_template("index.html")
@app.route("/login", methods=["POST"])
def login():
    email = request.json.get("email")
    password = request.json.get("password")
    role = request.json.get("role")

    print(email, password, role)

    return jsonify(True)
    
@app.route("/role")
def role():
    role = current_user.roles[0].name
    return jsonify(role) 

@auth_required('token')
@roles_required('manager', 'operator')
@app.route("/shgID/<int:meeting_id>")
def shgID(meeting_id):
    shg_id = db.session.query(meetings.shg_id).filter(meetings.id == meeting_id).first()[0]
    return jsonify({"shg_id" : shg_id})
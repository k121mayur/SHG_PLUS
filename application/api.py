from application.database import db
from application.models import Users, Sections, Books, Books_Authors, Books_Lendings, Authors, Requests
from flask import current_app as app, jsonify, request
from flask_restful import Resource
from flask_restful import fields, marshal_with, marshal_with_field
from flask_restful import reqparse
from flask_security import auth_required, roles_required, hash_password
from jwt import decode
from email_validator import validate_email
from datetime import datetime
from sqlalchemy import func
from application.app import user_datastore


class userApi(Resource):

    def get(self, user_id):
        pass

    def delete(self, username, password):
       pass
 
          

    def put(self):
       pass

      
    def post(self):
      data = request.json
      email = data.get('email')
      highest_id = db.session.query(Users.id).order_by(Users.id.desc()).limit(1).first()
      max_id = highest_id[0] + 1
      print(id)
      print(data.get("password"))
      try:
        validation = validate_email(email)
        email = validation.email
        print(email)
      except:
        return "", 404
      if not user_datastore.find_user(email=email):
        user_datastore.create_user(id = max_id, first_name=data.get('firstName'), last_name=data.get('lastName'), email=email, password=hash_password(data.get('password')),  last_login=datetime.now(), roles=['user'], date_created=datetime.now())
      db.session.commit()
      return jsonify(True)
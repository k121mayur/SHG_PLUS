from application.database import db
from application.models import *
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

class shgApi(Resource):

    def get(self):
       all_shgs = SHG.shg_name.query.all()
       return jsonify(all_shgs)
    
    @auth_required('token')
    @roles_required('manager', 'operator')
    def post(self):
        data = request.json
        
        # Extracting data from the JSON payload
        shg_name = data.get('name_of_shg')
        project_name = data.get('project_name')
        village_name = data.get('village_name')
        panchayat_name = data.get('panchyat_name')
        group_address = data.get('group_address')
        formation_date = datetime.strptime(data.get('formation_date'), "%Y-%m-%d").date()
        total_no_of_members = data.get('total_no_of_members')
        saving_day = data.get('saving_day')
        place_of_meeting = data.get('place_of_meeting')
        staff_name = data.get('staff_name')
        samuh_sakhi_name = data.get('samuh_sakhi_name')
        bank_name = data.get('bank_name')
        branch = data.get('branch')
        account_name = data.get('account_name')
        account_number = data.get('account_number')
        IFSC_code = data.get('IFSC_code')
        per_share_size_in_INR = data.get('per_share_size_in_INR')
        
        # Create a new SHG object
        new_shg = SHG(
            shg_name=shg_name,
            project_name=project_name,
            village_name=village_name,
            panchayat_name=panchayat_name,
            group_address=group_address,
            formation_date=formation_date,
            total_no_of_members=total_no_of_members,
            saving_day=saving_day,
            place_of_meeting=place_of_meeting,
            staff_name=staff_name,
            samuh_sakhi_name=samuh_sakhi_name,
            per_share_size_in_INR=per_share_size_in_INR
        )
        
        # Add the new SHG object to the database session
        db.session.add(new_shg)
        
        try:
            # Commit the transaction to persist the changes to the database
            db.session.commit()

            shg_id = db.session.query(SHG.id).filter(SHG.shg_name == shg_name).first()[0]

            new_bank_account = shgBankAccount(
                shg_id=shg_id,
                account_type='Savings',
                bank_name=bank_name,
                branch=branch,
                account_name=account_name,
                account_number=account_number,
                IFSC_code=IFSC_code
            )

            db.session.add(new_bank_account)
            try :
                db.session.commit()
                return {'message': 'SHG data saved successfully'}, 200
            except Exception as e:
                # Rollback the transaction in case of any error
                db.session.rollback()
                return {'message': f'Error saving bank account data: {str(e)}'}, 500
            
        except Exception as e:
            # Rollback the transaction in case of any error
            db.session.rollback()
            return {'message': f'Error saving SHG data: {str(e)}'}, 500
      
class memberApi(Resource):
   def post(self):
      pass
   
class shgBankAccountApi(Resource):
   def post(self):
      pass



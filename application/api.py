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
       all_shgs = db.session.query(SHG).all()
       all_shgs = [{'name': shg.shg_name, 'value': shg.id, 'village' : shg.village_name} for shg in all_shgs]
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
       data = request.json
       new_member = members(
            shg_id=data['shg_name']['value'],  # Assuming `id` is the correct identifier
            village=data['village'],
            household_code=data['household_code'],
            first_name=data['first_name'],
            father_husband_name=data['father_husband_name'],
            last_name=data['last_name'],
            number_of_family_members=data['number_of_family_members'],
            voter_id=data['voter_id'],
            adhar_id=data['adhar_id'],
            pan_number=data['pan_number'],
            ration_card_number=data['ration_card_number'],
            education=data['education'],
            category= data['category'],  # Convert list to comma-separated string
            caste=data['caste'],
            mobile_number=data['mobile_number'],
            total_land_kattha=data['total_land_kattha'],
            total_irrigated_land_kattha=data['total_irrigated_land_kattha'],
            total_no_of_goats=data['total_no_of_goats'],
            total_no_of_cattle=data['total_no_of_cattle'],
            total_no_of_members_migrated=data['total_no_of_members_migrated'],
            main_source_of_income=data['main_source_of_income'],
            head_of_the_family_name=data['head_of_the_family_name'],
            scheme_1=data['scheme_1'],
            scheme_2=data['scheme_2'],
  

            total_savings=0,
            loan_outstanding=0,
            interest_outstanding=0
        )

       db.session.add(new_member)
       try :
         mem_id = db.session.query(members.member_id).filter(members.shg_id == data['shg_name']['value']).first()[0]
         member_account = memberBankAccount(
            member_id=mem_id,
            account_type='Savings',
            bank_name=data['bank_name'],
            branch=data['branch_name'],
            account_name= data['first_name'] + ' ' + data['father_husband_name'] + ' ' + data['last_name'],
            account_number=data['account_number'],
            IFSC_code=data['IFSC_code']
         )
         db.session.add(member_account)
         db.session.commit()
       except Exception as e:
         # Rollback the transaction in case of any error
         db.session.rollback()
         return {'message': f'Error saving member data: {str(e)}'}, 500

       return jsonify({"status": True})
    
   def get(self, shg_id):
        members_list = db.session.query(members).filter(members.shg_id == shg_id).all()
        members_list = [{'name': member.first_name + ' ' + member.father_husband_name + ' ' + member.last_name, 'value': member.member_id} for member in members_list]

        return jsonify(members_list)


   
class shgBankAccountApi(Resource):
   def post(self):
      pass



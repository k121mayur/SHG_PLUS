from application.database import db
from application.models import *
from flask import current_app as app, jsonify, request
from flask_restful import Resource
from flask_restful import fields, marshal_with, marshal_with_field
from flask_restful import reqparse
from flask_security import auth_required, roles_required, hash_password
from email_validator import validate_email
from datetime import datetime
from sqlalchemy import func
from application.app import user_datastore
from sqlalchemy import func


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
    @auth_required('token')
    @roles_required('manager', 'operator')
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
   
   def get(self, shg_id=None, meeting_id=None):
        if shg_id:
            return self.get_by_shg_id(shg_id)
        elif meeting_id:
            return self.get_by_meeting_id(meeting_id)
        else:
            return {'message': 'Invalid request'}, 400
    
   def get_by_shg_id(self, shg_id):
        members_list = db.session.query(members).filter(members.shg_id == shg_id).all()
        members_list = [{'name': member.first_name + ' ' + member.father_husband_name + ' ' + member.last_name, 'value': member.member_id} for member in members_list]

        return jsonify(members_list)
   
   # List of members present in the meeting
   def get_by_meeting_id(self, meeting_id):
        print("Meeting Id call", meeting_id)
        members_id = db.session.query(meetingAttendence.member_id).filter(meetingAttendence.meeting_id == meeting_id).filter(meetingAttendence.attended == 1).all()
        members_list = []
        for member_id in members_id:
            member = db.session.query(members).filter(members.member_id == member_id[0]).first()
            members_list.append({'name': member.first_name + ' ' + member.father_husband_name + ' ' + member.last_name, 'value': member.member_id})

        return jsonify(members_list)

class shgBankAccountApi(Resource):
   def post(self):
      pass

   def get(self, shg_id, account_type):
      if account_type == 0:
         account_type = 'loan'
      elif account_type == 1:
         account_type = 'savings'
      accounts = db.session.query(shgBankAccount).filter(shgBankAccount.shg_id == shg_id).filter(shgBankAccount.account_type == account_type).all()
      account_list = []
      for account in accounts:
          account_list.append({
            'id': account.id,
            'bank_name': account.bank_name,
            'branch': account.branch,
            'account_name': account.account_name,
            'account_number': account.account_number,
            'IFSC_code': account.IFSC_code,
            'balance': account.balance
          })
      return jsonify(account_list)
         

class meetingApi(Resource):
   def post(self):
      try:
        data = request.json
        attendece = 0
        for i in data['attendece']:
          if i['present']:
              attendece += 1
        if attendece == 0:
          return {'message': 'Atlease one member should be present in the meeting to add Group Meeting'}, 400
        new_meeting = meetings(
              shg_id=data['shg']['value'],  # Assuming `id` is the correct identifier
              meeting_date = datetime.strptime(data['date'], "%Y-%m-%d").date(), 
              attendece = attendece,
              conducted = True if attendece > 0 else False
          )
        db.session.add(new_meeting)

        max_id = meetings.query.with_entities(func.max(meetings.id)).first()
        max_id = max_id[0]
        for a in data['attendece']:
          member_attendece = meetingAttendence(
                member_id = a['value'],
                meeting_id = max_id, 
                attended = a['present']
          )

          db.session.add(member_attendece)
        
        db.session.commit()
      except Exception as e:
        # Rollback the transaction in case of any error
        db.session.rollback()
        return {'message': f'Error saving meeting data: {str(e)}'}, 500
      return jsonify({"status": True, "meeting_id": max_id})
   
   def get(self, shg_id):
        print(shg_id)
        meetings_list = meetings.query.filter(meetings.shg_id == shg_id).all()
        print(meetings_list)
        meetings_list = [{'name': datetime.strftime(meeting.meeting_date, "%d-%m-%Y"), 'date': meeting.meeting_date, 'value': meeting.id} for meeting in meetings_list]

        return jsonify(meetings_list)   
      
class memberReceiptApi(Resource):
   def post(self):
      data = request.json
      meeting_id = data['meeting_id']
      member_id = data['member_id']
      
      receipts = {"savings" : data['savings'], 
                  "principal" : data['principal'], 
                  "interest" : data['interest'], 
                  "fine" : data['fine'] }
      
      receipt_date = db.session.query(meetings.meeting_date).filter(meetings.id == meeting_id).first()[0]

      for type, amt in receipts.items():
        if int(amt) > 0 and type == "savings":
           new_saving_receipt = memberSavingsReceipts(
            meeting_id = meeting_id,
            member_id = member_id,
            receipt_date = receipt_date,
            receipt_amount = amt
           )
           db.session.add(new_saving_receipt)
        
        elif int(amt) > 0 and type == "principal":
           new_loan_receipt = memberLoanRepaymentReceipts(
            meeting_id = meeting_id,
            member_id = member_id,
            receipt_date = receipt_date,
            principal_amount = amt, 
            interest_amount = data['interest']
           )
           db.session.add(new_loan_receipt)
        elif int(amt) > 0 and type == "fine":
           new_fine_receipt = memberFineReceipts(
            meeting_id = meeting_id,
            member_id = member_id,
            receipt_date = receipt_date,
            receipt_amount = amt
           )
           db.session.add(new_fine_receipt) 
        else:
           continue   
      db.session.commit()
      
      return jsonify({"message": "Receipt added successfully."})


class otherLoanReceiptsApi(Resource):
   def post(self):
      data = request.json
      meeting_id = data['meeting_id']
      receipt_date = db.session.query(meetings.meeting_date).filter(meetings.id == meeting_id).first()[0]
      LoanAccountId = data['loanAccountId']
      loanType = data['loanType']
      loanAmount = data['loanAmount']
      tenure =  data['tenure']
      interestRate = data['interestRate'] 

      new_receipt = otherLoanReceipts(
      meeting_id = meeting_id,
      loan_account_id = LoanAccountId,
      loan_type = loanType,
      loan_amount = loanAmount,
      loan_date = receipt_date,
      loan_tenure = tenure,
      loan_interest_rate = interestRate
      )
      db.session.add(new_receipt)
      db.session.commit()
      return jsonify({"message": "Loan Receipt added successfully."})


class otherSavingsReceiptsApi(Resource):
   def post(self):
      data = request.json
      meeting_id = data['meeting_id']

      savingsAccountId = data['savingsAccountId']
      withdrawalDate = data['withdrawalDate']
      withdrawalAmount = data['withdrawalAmount']

      new_receipt = otherSavingsReceipts(
      meeting_id = meeting_id,
      savings_account_id = savingsAccountId,
      withdrawal_date = datetime.strptime(withdrawalDate, '%Y-%m-%d').date(),
      withdrawal_amount = withdrawalAmount
      )
      db.session.add(new_receipt)
      db.session.commit()
      return jsonify({"message": "Bank Withdrawal Receipt added successfully."})


      db.session.add(new_receipt)
      db.session.commit()
      return jsonify({"message": "Savings Receipt added successfully."})



class memberPaymentsApi(Resource):
   def post(self):
      pass

class otherPaymentsApi(Resource):
   def post(self):
      pass


class loanPurposeListApi(Resource):
   def get(self):
      loan_purpose_list = db.session.query(loanPurposeList).all()
      loan_purpose_list = [{'name': purpose.loan_purpose, 'value': purpose.id} for purpose in loan_purpose_list]
      return jsonify(loan_purpose_list)
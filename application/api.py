from application.database import db
from application.models import *
from flask import current_app as app, jsonify, request
from flask_restful import Resource
from flask_restful import fields, marshal_with, marshal_with_field
from flask_restful import reqparse
from flask_security import auth_required, roles_required, hash_password, verify_password
from email_validator import validate_email
from datetime import datetime
from sqlalchemy import func
from application.app import user_datastore
from application.controllers import internal_meeting_status


class userApi(Resource):
  

    def get(self, user_id):
        pass

    def delete(self, email):
       user = user_datastore.find_user(email=email)
       if user :
          user_datastore.delete_user(user)
          db.session.commit()
          return jsonify(True)
       else:
          return jsonify(False)
 

    def put(self, email_id):
       user = user_datastore.find_user(email=email_id)
       if user :
         if verify_password(request.json.get('old_password'), user.password):
            user.password = hash_password(request.json.get('new_password'))
            db.session.commit()
            return jsonify(True)
         else:
            return jsonify(False)
       else:
          return jsonify(True)
   
      
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
        user_datastore.create_user(id = max_id, first_name=data.get('first_name'), last_name=data.get('last_name'), email=email, password=hash_password(data.get('password')),  last_login=datetime.now(), roles=[data.get('role')], date_created=datetime.now())
        db.session.commit()
        return jsonify(True)
      else:
        return jsonify(False)
      

class shgApi(Resource):
   #  @auth_required('token')
   #  @roles_required('manager', 'operator')
    def get(self, month=None):
       if month:
           return self.get_by_month(month)
       else:
          all_shgs = db.session.query(SHG).all()
          all_shgs = [{'name': shg.shg_name, 'value': shg.id, 'village' : shg.village_name} for shg in all_shgs]
          return jsonify(all_shgs)
       

    def get_by_month(self, month):
       print(month)
       all_meetings = db.session.query(meetings).filter(func.strftime('%m', meetings.meeting_date) == f'{month:02d}').all()
       print(all_meetings)
       data = []

       for meeting in all_meetings:
          
          status = internal_meeting_status(meeting.id)
          date_format = datetime.strptime(str(meeting.meeting_date), "%Y-%m-%d").strftime("%d-%m-%Y")
          data.append({
            "id" : meeting.id,
            "name" : db.session.query(SHG.shg_name).filter(SHG.id == meeting.shg_id).first()[0],
            "date"  : date_format,  
            "status" : status["meeting_status"],
            "action": "Entry" if status["status_class"] == "text-danger" else "Completed",
          })

       return jsonify(data)
      
   

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
        first_saving_date = datetime.strptime(data.get('first_saving_date'), "%Y-%m-%d").date()
        total_no_of_members = data.get('total_no_of_members')
        saving_day = data.get('saving_day')
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
            first_saving_date=first_saving_date,
            total_no_of_members=total_no_of_members,
            saving_day=saving_day,
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

            if account_number:
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

         ayushyman_bharat = data['Ayushman_Bharat']
         pmjjby = data['PMJJBY']
         pmsby = data['PMSBY']
         labour_card = data['Labour_card']



         if ayushyman_bharat:
           scheme_id = db.session.query(schemes.id).filter(schemes.scheme_name == "Ayushman Bharat").first()[0]
           scheme_enrollment = schemeMemberEnrollment(
             member_id=mem_id,
             scheme_id=scheme_id
           )
           db.session.add(scheme_enrollment)

         if pmjjby:
           scheme_id = db.session.query(schemes.id).filter(schemes.scheme_name == "Pradhan Mantri Jivan Jyoti Bima Yojana").first()[0]
           scheme_enrollment = schemeMemberEnrollment(
             member_id=mem_id,
             scheme_id=scheme_id
           )
           db.session.add(scheme_enrollment)

         if pmsby:
           scheme_id = db.session.query(schemes.id).filter(schemes.scheme_name == "Pradhan Mantri Surksha Bima Yojana").first()[0]
           scheme_enrollment = schemeMemberEnrollment(
             member_id=mem_id,
             scheme_id=scheme_id
           )
           db.session.add(scheme_enrollment)

         if labour_card:
           scheme_id = db.session.query(schemes.id).filter(schemes.scheme_name == "Labour Card").first()[0]
           scheme_enrollment = schemeMemberEnrollment(
             member_id=mem_id,
             scheme_id=scheme_id
           )
           db.session.add(scheme_enrollment)

         db.session.commit()
       except Exception as e:
         # Rollback the transaction in case of any error
         db.session.rollback()
         return {'message': f'Error saving member data: {str(e)}'}, 500

       return jsonify({"message": "Member added successfully"})
   
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
   #    __tablename__ = 'shgBankAccount'
   #  id = db.Column(db.Integer, primary_key=True)
   #  account_type = db.Column(db.String(10), nullable=False)
   #  bank_name = db.Column(db.String(100), nullable=False)
   #  branch = db.Column(db.String(100), nullable=False)
   #  account_name = db.Column(db.String(100), nullable=False)
   #  account_number = db.Column(db.String(50), nullable=False)
   #  IFSC_code = db.Column(db.String(20), nullable=False)
   #  shg_id = db.Column(db.Integer, db.ForeignKey('shg.id'), nullable=False)
   #  balance = db.Column(db.Integer, nullable=False, default=0)

      data = request.json
      account = shgBankAccount(
         account_type=data['account_type'] if data['account_type'] else "loan",
         bank_name=data['bank_name'],
         branch=data['branch_name'],
         account_name=db.session.query(SHG.shg_name).filter(SHG.id == data['shg_id']).first()[0],
         account_number=data['account_number'],
         IFSC_code=data['ifsc_code'],
         shg_id=data['shg_id'],
         balance=0,
      )
      db.session.add(account)
      db.session.commit()
      return jsonify({"status": True})

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
           try:
              new_saving_receipt = memberSavingsReceipts(
              meeting_id = meeting_id,
              member_id = member_id,
              receipt_date = receipt_date,
              receipt_amount = amt
               )
              db.session.add(new_saving_receipt)

              current_saving = db.session.query(members.total_savings).filter(members.member_id == member_id).first()[0]
              new_saving = current_saving + int(amt)
              db.session.query(members).filter(members.member_id == member_id).update({members.total_savings : new_saving})

           except Exception as e:
              return jsonify({"message": "Double Entry Error", "error": "Internal Server Error"})
           
        
        elif int(amt) > 0 and type == "principal": #principal
           print("principal")
           new_loan_receipt = memberLoanRepaymentReceipts(
            meeting_id = meeting_id,
            member_id = member_id,
            receipt_date = receipt_date,
            principal_amount = amt, 
            interest_amount = data['interest']
           )
           
           current_loan = db.session.query(members.loan_outstanding).filter(members.member_id == member_id).first()[0]
           current_interest = db.session.query(members.interest_outstanding).filter(members.member_id == member_id).first()[0]
           new_loan = current_loan - int(amt)
           new_interest = current_interest - int(data['interest'])
           if amt < current_loan and current_loan > 0:
              db.session.add(new_loan_receipt)
              db.session.query(members).filter(members.member_id == member_id).update({members.loan_outstanding : new_loan})
           
           else:
              return jsonify({"message": "Principal amount should be less than outstanding loan amount. Rs. " + str(current_loan) + " is outstanding."})
           
           if int(data['interest']) < current_interest and current_interest > 0:
              db.session.query(members).filter(members.member_id == member_id).update({members.interest_outstanding : new_interest})
           else:
              return jsonify({"message": "Interest amount should be less than outstanding interest amount. Rs. " + str(current_interest) + " is outstanding."})

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
      try:  
         db.session.commit()
      except:
         return jsonify({"message": "For this member receipt already exist. Edit or Delete earlier receipt."})
      return jsonify({"message": "Receipt added successfully."})

   def get(self, meeting_id):
      #Wrtite code here to get receipt details
      members_attendece = db.session.query(meetingAttendence).filter(meetingAttendence.meeting_id == meeting_id, meetingAttendence.attended == 1).all()
      data = []
      for member in members_attendece:
          
          savings_receipt = db.session.query(memberSavingsReceipts).filter(memberSavingsReceipts.meeting_id == meeting_id, memberSavingsReceipts.member_id == member.member_id).first()
          
          principal_receipt = db.session.query(memberLoanRepaymentReceipts).filter(memberLoanRepaymentReceipts.meeting_id == meeting_id, memberLoanRepaymentReceipts.member_id == member.member_id).first()
          
          fine_receipts = db.session.query(memberFineReceipts).filter(memberFineReceipts.meeting_id == meeting_id, memberFineReceipts.member_id == member.member_id).first()
          
          member_data = db.session.query(members).filter(members.member_id == member.member_id).first()
          
          data.append({'id': member.member_id, 'name': member_data.first_name + ' ' + member_data.father_husband_name + ' ' + member_data.last_name, 
                       'savings': [savings_receipt.receipt_amount, savings_receipt.id] if savings_receipt else [0, 0], 
                       'principal': [principal_receipt.principal_amount, principal_receipt.id] if principal_receipt else [0, 0],
                       'interest': [principal_receipt.interest_amount, principal_receipt.id] if principal_receipt else [0, 0],
                       'fine':[fine_receipts.receipt_amount, fine_receipts.id] if fine_receipts else [0, 0]})
      print(data)
      return jsonify(data)

   def delete(self):
      savings_id = request.json['savings']
      principal_id = request.json['principal']
      interest_id = request.json['interest']
      fine_id = request.json['fine']
      member_id = request.json['member_id']

      if savings_id > 0:
         current_total_saving = db.session.query(members.total_savings).filter(members.member_id == member_id).first()[0]
         receipt_amt = db.session.query(memberSavingsReceipts.receipt_amount).filter(memberSavingsReceipts.id == savings_id).first()[0]
         new_saving = current_total_saving - receipt_amt
         db.session.query(members).filter(members.member_id == member_id).update({members.total_savings : new_saving})
         db.session.query(memberSavingsReceipts).filter(memberSavingsReceipts.id == savings_id).delete()
      
      if principal_id > 0:
         principal_amt = db.session.query(memberLoanRepaymentReceipts.principal_amount).filter(memberLoanRepaymentReceipts.id == principal_id).first()[0]
         
         current_loan = db.session.query(members.loan_outstanding).filter(members.member_id == member_id).first()[0]
         new_loan = current_loan - principal_amt
         
         db.session.query(members).filter(members.member_id == member_id).update({ members.loan_outstanding : new_loan})
         db.session.query(memberLoanRepaymentReceipts).filter(memberLoanRepaymentReceipts.id == principal_id).delete()
      
      if interest_id > 0:
         interest_amt = db.session.query(memberLoanRepaymentReceipts.interest_amount).filter(memberLoanRepaymentReceipts.id == principal_id).first()[0]
         new_interest = db.session.query(members.interest_outstanding).filter(members.member_id == member_id).first()[0] - interest_amt
         db.session.query(members).filter(members.member_id == member_id).update({members.interest_outstanding : new_interest})
         db.session.query(memberLoanRepaymentReceipts).filter(memberLoanRepaymentReceipts.id == interest_id).delete()
      if fine_id > 0:
         db.session.query(memberFineReceipts).filter(memberFineReceipts.id == fine_id).delete()
      
      db.session.commit()
      return jsonify({"message": "Receipt deleted successfully."})

class otherLoanReceiptsApi(Resource):
   def post(self):
      data = request.json
      meeting_id = data['meeting_id']
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
      loan_date = datetime.strptime(data['loanDate'], "%Y-%m-%d").date(),
      loan_tenure = tenure,
      loan_interest_rate = interestRate
      )
      db.session.add(new_receipt)

      loan_account = db.session.query(shgBankAccount).filter(shgBankAccount.id == LoanAccountId).first()
      loan_account.balance = loan_account.balance + loanAmount

      db.session.commit()
      return jsonify({"message": "Loan Receipt added successfully."})
   
   def get(self, meeting_id):
      #Wrtite code here to get receipt details by meeting id
      other_loan_receipts = db.session.query(otherLoanReceipts).filter(otherLoanReceipts.meeting_id == meeting_id).all()
      data = []
      for receipt in other_loan_receipts:
         data.append({"id": receipt.id, 'bank': db.session.query(shgBankAccount.bank_name).filter(shgBankAccount.id == receipt.loan_account_id).first()[0], 'loanType': receipt.loan_type, 'loanAmount': receipt.loan_amount, 'tenure': receipt.loan_tenure, 'interestRate': receipt.loan_interest_rate})
      return jsonify(data)

   def delete(self):
      id = request.json['id']
      receipt = db.session.query(otherLoanReceipts).filter(otherLoanReceipts.id == id)

      loan_account = db.session.query(shgBankAccount).filter(shgBankAccount.id == receipt.loan_account_id).first()
      loan_account.balance = loan_account.balance - receipt.loan_amount

      receipt.delete()
      db.session.commit()
      return jsonify({"message": "Receipt deleted successfully."})

class otherSavingsReceiptsApi(Resource):
   def post(self):
      data = request.json
      meeting_id = data['meeting_id']

      savingsAccountId = data['savingsAccountId']
      withdrawalDate = data['withdrawalDate']
      withdrawalAmount = data['withdrawalAmount']

      savings_account = db.session.query(shgBankAccount).filter(shgBankAccount.id == savingsAccountId).first()
      if savings_account.balance < withdrawalAmount:
         return jsonify({"message": "Insufficient balance in savings account. Can't make withdrawal."})
      
      new_receipt = otherSavingsReceipts(
      meeting_id = meeting_id,
      savings_account_id = savingsAccountId,
      withdrawal_date = datetime.strptime(withdrawalDate, '%Y-%m-%d').date(),
      withdrawal_amount = withdrawalAmount
      )
      db.session.add(new_receipt)
      savings_account.balance = savings_account.balance - withdrawalAmount
      
      db.session.commit()
      return jsonify({"message": "Bank Withdrawal Receipt added successfully."})

   def get(self, meeting_id):
      #Wrtite code here to get receipt details by meeting id
      other_savings_receipts = db.session.query(otherSavingsReceipts).filter(otherSavingsReceipts.meeting_id == meeting_id).all()
      data = []
      for receipt in other_savings_receipts:
         data.append({"id": receipt.id, 'bank': db.session.query(shgBankAccount.bank_name).filter(shgBankAccount.id == receipt.savings_account_id).first()[0], 'withdrawalAmount': receipt.withdrawal_amount, 'withdrawalDate': receipt.withdrawal_date.strftime('%d-%b-%Y')})
      return jsonify(data)

   def delete(self):
      id = request.json['id']
      receipt = db.session.query(otherSavingsReceipts).filter(otherSavingsReceipts.id == id)

      shg_account = db.session.query(shgBankAccount).filter(shgBankAccount.id == receipt.savings_account_id).first()
      shg_account.balance = shg_account.balance + receipt.withdrawal_amount

      receipt.delete()
      db.session.commit()
      return jsonify({"message": "Receipt deleted successfully."})

class otherCashInBoxReceiptsApi(Resource):
   def post(self):
      data = request.json
      meeting_id = data['meeting_id']
      receipt_date = db.session.query(meetings.meeting_date).filter(meetings.id == meeting_id).first()[0]
      receipt_amount = data['cash_in_hand_amt']
      shg_id = db.session.query(meetings.shg_id).filter(meetings.id == meeting_id).first()[0]
      print(shg_id)
      shg_this = db.session.query(SHG).filter(SHG.id == shg_id).first()
      print(shg_this)
      if receipt_amount > shg_this.cash_in_box:
         return jsonify({"message": "Receipt amount cannot be greater than cash in box amount."})


      new_receipt = otherCashInBoxReceipts(
      meeting_id = meeting_id,
      receipt_date = receipt_date,
      receipt_amount = receipt_amount,
      )
      db.session.add(new_receipt)
      
      shg_this.cash_in_box = shg_this.cash_in_box - receipt_amount

      db.session.commit()
      return jsonify({"message": "Receipt added successfully."})
   
   def get(self, meeting_id):
      other_cash_in_hand_receipts = db.session.query(otherCashInBoxReceipts).filter(otherCashInBoxReceipts.meeting_id == meeting_id).all()
      data = []
      for receipt in other_cash_in_hand_receipts:
         data.append({"id": receipt.id, 'amount': receipt.receipt_amount})
      return jsonify(data)

   def delete(self):
      id = request.json['id']
      receipt = db.session.query(otherCashInBoxReceipts).filter(otherCashInBoxReceipts.id == id)
      shg_id = db.session.query(meetings.shg_id).filter(meetings.meeting_id == receipt.meeting_id).first()[0]
      shg = db.session.query(SHG).filter(SHG.id == shg_id).first()
      shg.cash_in_box = shg.cash_in_box + receipt.receipt_amount
      db.session.commit()
      return jsonify({"message": "Receipt deleted successfully."})

class memberLoanPaymentsApi(Resource):
   def post(self):
      data = request.json
      meeting_id = data['meeting_id']
      member_id = data['member_id']
      receipt_date = datetime.strptime(data['loan_date'], "%Y-%m-%d").date()
      
      new_receipt = memberLoanPayments(
         meeting_id = meeting_id,
         member_id = member_id,
         payment_date = receipt_date,
         payment_amount = data['loan_amount'],
         loan_purpose = data['loan_purpose']
      )
      db.session.add(new_receipt)

      member = db.session.query(members).filter(members.member_id == member_id).first()
      member.loan_outstanding += data['loan_amount']
      db.session.commit()
   def get(self, meeting_id):
      member_loan_payments = db.session.query(memberLoanPayments).filter(memberLoanPayments.meeting_id == meeting_id).all()
      data = []
      for receipt in member_loan_payments:
         data.append({"id": receipt.id, 
                      'name': db.session.query(members.first_name).filter(members.member_id == receipt.member_id).first()[0]+ " " + db.session.query(members.last_name).filter(members.member_id == receipt.member_id).first()[0] , 'payment_type': "Loan", 'payment_amount': receipt.payment_amount,})
      return jsonify(data)

   def delete(self):
      id = request.json['id']
      receipt = db.session.query(memberLoanPayments).filter(memberLoanPayments.id == id)

      member = db.session.query(members).filter(members.member_id == receipt.member_id).first()
      member.loan_outstanding -= receipt.payment_amount

      receipt.delete()
      db.session.commit()
      return jsonify({"message": "Receipt deleted successfully."})


class memberSavingsPaymentsApi(Resource):
   def post(self):
      data = request.json
      meeting_id = data['meeting_id']
      member_id = data['member_id']
      receipt_date = db.session.query(meetings.meeting_date).filter(meetings.id == meeting_id).first()[0]
      
      new_receipt = memberSavingsPayments(   
         meeting_id = meeting_id,
         member_id = member_id,
         payment_date = receipt_date,
         payment_amount = data['savings_return_amount'],
         reason = data['savingsReturnReason']
      )

      db.session.add(new_receipt)
      db.session.commit()
      return jsonify({"message": "Receipt added successfully."})

   def get(self, meeting_id):
      member_savings_payments = db.session.query(memberSavingsPayments).filter(memberSavingsPayments.meeting_id == meeting_id).all()
      data = []
      for receipt in member_savings_payments:
         data.append({"id": receipt.id, "name": db.session.query(members.first_name).filter(members.member_id == receipt.member_id).first()[0] + " " +db.session.query(members.last_name).filter(members.member_id == receipt.member_id).first()[0], 
                      "payment_type": "Savings", "payment_amount": receipt.payment_amount})

      return jsonify(data)
   
   def delete(self):
      id = request.json['id']
      db.session.query(memberSavingsPayments).filter(memberSavingsPayments.id == id).delete()
      db.session.commit()
      return jsonify({"message": "Receipt deleted successfully."})

class bankEmiPaymentsApi(Resource):
   def post(self):
      data = request.json
      meeting_id = data['meeting_id']
      receipt_date = datetime.strptime(data['Date'], "%Y-%m-%d").date()
      
      new_receipt = bankEmiPayments(   
         meeting_id = meeting_id,
         loan_account_id = data['loanAccountId'],
         payment_date = receipt_date,
         principal_amount = data['Amount']
      )

      db.session.add(new_receipt)
      try:
         db.session.commit()
      except:
         db.session.rollback()
         return "Error", 500
      
      return jsonify({"message": "Receipt added successfully."})
   def get(self, meeting_id):
      bank_emi_payments = db.session.query(bankEmiPayments).filter(bankEmiPayments.meeting_id == meeting_id).all()
      data = []
      for receipt in bank_emi_payments:
         data.append({"id": receipt.id, "payment_type": "Loan Repayment", "payment_amount": receipt.principal_amount})
      return jsonify(data)

   def delete(self):
      id = request.json['id']
      db.session.query(bankEmiPayments).filter(bankEmiPayments.id == id).delete()
      db.session.commit()
      return jsonify({"message": "Receipt deleted successfully."})

class savingsAccountPaymentsApi(Resource):
   def post(self):
      data = request.json

      meeting_id = data['meeting_id']
      receipt_date = db.session.query(meetings.meeting_date).filter(meetings.id == meeting_id).first()[0]
      
      new_receipt = savingsAccountPayments(   
         meeting_id = meeting_id,
         savings_account_id = data['savingsAccountId'],
         payment_date = receipt_date,
         payment_amount = data['depositAmount']
      )

      try: 
         if db.session.add(new_receipt) == None:
            account = db.session.query(shgBankAccount).filter(shgBankAccount.id == data['savingsAccountId']).first()
            account.balance += data['depositAmount']
            db.session.commit()
            return jsonify({"message": "Receipt added successfully."})
      except:
         db.session.rollback()
         return "Error", 500
      
   def get(self, meeting_id):
      savings_account_payments = db.session.query(savingsAccountPayments).filter(savingsAccountPayments.meeting_id == meeting_id).all()
      data = []
      for receipt in savings_account_payments:
         data.append({"id": receipt.id, "payment_type": "Savings Deposites", "payment_amount": receipt.payment_amount})
      return jsonify(data)
   
   def delete(self):
      id = request.json['id']
      receipt = db.session.query(savingsAccountPayments).filter(savingsAccountPayments.id == id).first()
      account = db.session.query(shgBankAccount).filter(shgBankAccount.id == receipt.savings_account_id).first()
      account.balance -= receipt.payment_amount
      receipt.delete()
      db.session.commit()
      return jsonify({"message": "Receipt deleted successfully."})

class otherServiceChargePaymentsApi(Resource):
   def post(self):
      data = request.json
      meeting_id = data['meeting_id']
      member_id = data['service_charge_member_id']
      receipt_date = db.session.query(meetings.meeting_date).filter(meetings.id == meeting_id).first()[0]
      
      new_receipt = otherServiceChargePayments(   
         meeting_id = meeting_id,
         member_id = member_id,    
         payment_date = receipt_date,   
         payment_amount = data['service_charge_amount']
      )

      db.session.add(new_receipt)
      db.session.commit()
      return jsonify({"message": "Receipt added successfully."})
   def get(self, meeting_id):
      other_service_charge_payments = db.session.query(otherServiceChargePayments).filter(otherServiceChargePayments.meeting_id == meeting_id).all()
      data = []
      for receipt in other_service_charge_payments:
         data.append({"id": receipt.id, "payment_type": "Service Charge", "payment_amount": receipt.payment_amount})
      return jsonify(data)

   def delete(self):
      id = request.json['id']
      db.session.query(otherServiceChargePayments).filter(otherServiceChargePayments.id == id).delete()
      db.session.commit()
      return jsonify({"message": "Receipt deleted successfully."})
   
class otherCashInBoxPaymentsApi(Resource):
   def post(self):
      data = request.json
      meeting_id = data['meeting_id']
      receipt_date = db.session.query(meetings.meeting_date).filter(meetings.id == meeting_id).first()[0]
      
      new_receipt = otherCashInBoxPayments(
         meeting_id = meeting_id,
         payment_date = receipt_date,
         payment_amount = data['cash_in_hand_amount']
      )

      db.session.add(new_receipt)

      shg_id = db.session.query(meetings.shg_id).filter(meetings.id == meeting_id).first()[0]
      shg = db.session.query(SHG).filter(SHG.id == shg_id).first()
      shg.cash_in_box += data['cash_in_hand_amount']
      db.session.commit()
      return jsonify({"message": "Receipt added successfully."})
   def get(self, meeting_id):
      other_cash_in_hand_payments = db.session.query(otherCashInBoxPayments).filter(otherCashInBoxPayments.meeting_id == meeting_id).all()
      data = []
      for receipt in other_cash_in_hand_payments:
         data.append({"id": receipt.id,  "payment_type": "Cash In Box", "payment_amount": receipt.payment_amount})
      return jsonify(data)

   def delete(self):
      id = request.json['id']
      db.session.query(otherCashInBoxPayments).filter(otherCashInBoxPayments.id == id).delete()
      db.session.commit()
      return jsonify({"message": "Receipt deleted successfully."})

class loanPurposeListApi(Resource):
   def get(self):
      loan_purpose_list = db.session.query(loanPurposeList).all()
      loan_purpose_list = [{'name': purpose.loan_purpose, 'value': purpose.id} for purpose in loan_purpose_list]
      return jsonify(loan_purpose_list)
   
class operatorDashboardApi(Resource):
   def get(self):
      # Total Number of Groups
      all_active_groups = db.session.query(SHG).filter(SHG.active == True).all()
      total_number_of_groups = len(all_active_groups)

      # This month Entry completed
      entry_completed_groups = 0 

      this_month = datetime.now().month
      
      this_month_meeting_entry = db.session.query(meetings).filter(func.strftime('%m', meetings.meeting_date) == f'{this_month:02d}').all()
      
      for meeting in this_month_meeting_entry:
         if internal_meeting_status(meeting.id)['status_class'] == "text-success":
            entry_completed_groups += 1

      return jsonify({"number_of_groups": total_number_of_groups, "entry_completed_groups": entry_completed_groups})
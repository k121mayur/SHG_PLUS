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
from sqlalchemy import func

import time


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


@auth_required('token')
@roles_required('operator')
@app.route("/meeting_status/<int:meeting_id>")
def meeting_status(meeting_id):
    #Case 1 : Attendece and Member Receipts are not matching

    attendence = len(db.session.query(meetingAttendence).filter(meetingAttendence.meeting_id == meeting_id, meetingAttendence.attended == 1).all())
    print(attendence)
    member_receipts = [r.member_id for r in db.session.query(memberSavingsReceipts.member_id).filter(memberSavingsReceipts.meeting_id == meeting_id).all() ]
    loan_repayment_receipts = [r.member_id for r in db.session.query(memberLoanRepaymentReceipts.member_id).filter(memberLoanRepaymentReceipts.meeting_id == meeting_id).all() ]
    receipts = set(member_receipts + loan_repayment_receipts)
    print(receipts,member_receipts, loan_repayment_receipts)
    if len(receipts) != attendence:
        return jsonify({"meeting_status" : "Member receipts entry pending", "status_class" : "text-danger"})
    
    #Case 2 : The Receipts total vs Payment Total is not matching
    
    # Member Receipts
    savings_total =  db.session.query(func.sum(memberSavingsReceipts.receipt_amount)).filter(memberSavingsReceipts.meeting_id == meeting_id).first()[0]
    savings_total = savings_total if savings_total else 0
    
    principal_total = db.session.query(func.sum(memberLoanRepaymentReceipts.principal_amount)).filter(memberLoanRepaymentReceipts.meeting_id == meeting_id).first()[0]
    principal_total = principal_total if principal_total else 0
    
    interest_total = db.session.query(func.sum(memberLoanRepaymentReceipts.interest_amount)).filter(memberLoanRepaymentReceipts.meeting_id == meeting_id).first()[0]
    interest_total = interest_total if interest_total else 0
    
    fine_total = db.session.query(func.sum(memberFineReceipts.receipt_amount)).filter(memberFineReceipts.meeting_id == meeting_id).first()[0]
    fine_total = fine_total if fine_total else 0
    # Other Receipts
    loan_receipts_total = db.session.query(func.sum(otherLoanReceipts.loan_amount)).filter(otherLoanReceipts.meeting_id == meeting_id).first()[0]
    loan_receipts_total = loan_receipts_total if loan_receipts_total else 0
    
    bank_saving_receipts_total = db.session.query(func.sum(otherSavingsReceipts.withdrawal_amount)).filter(otherSavingsReceipts.meeting_id == meeting_id).first()[0]
    bank_saving_receipts_total = bank_saving_receipts_total if bank_saving_receipts_total else 0

    total_receipts = savings_total + principal_total + interest_total + fine_total + loan_receipts_total + bank_saving_receipts_total

    # Member Payments
    member_loan_total = db.session.query(func.sum(memberLoanPayments.payment_amount)).filter(memberLoanPayments.meeting_id == meeting_id).first()[0]
    member_loan_total = member_loan_total if member_loan_total else 0
    
    member_savings_return_total = db.session.query(func.sum(memberSavingsPayments.payment_amount)).filter(memberSavingsPayments.meeting_id == meeting_id).first()[0]
    member_savings_return_total = member_savings_return_total if member_savings_return_total else 0
    # Other Payments

    bank_emi_total = db.session.query(func.sum(bankEmiPayments.principal_amount)).filter(bankEmiPayments.meeting_id == meeting_id).first()[0]
    bank_emi_total = bank_emi_total if bank_emi_total else 0
    
    bank_emi_interest_total = db.session.query(func.sum(bankEmiPayments.interest_amount)).filter(bankEmiPayments.meeting_id == meeting_id).first()[0]
    bank_emi_interest_total = bank_emi_interest_total if bank_emi_interest_total else 0
    
    savings_account_payments_total = db.session.query(func.sum(savingsAccountPayments.payment_amount)).filter(savingsAccountPayments.meeting_id == meeting_id).first()[0]
    savings_account_payments_total = savings_account_payments_total if savings_account_payments_total else 0
    
    service_charge_payments_total = db.session.query(func.sum(otherServiceChargePayments.payment_amount)).filter(otherServiceChargePayments.meeting_id == meeting_id).first()[0]
    service_charge_payments_total = service_charge_payments_total if service_charge_payments_total else 0
    
    cash_in_hand_total = db.session.query(func.sum(otherCashInHandPayments.payment_amount)).filter(otherCashInHandPayments.meeting_id == meeting_id).first()[0]
    cash_in_hand_total = cash_in_hand_total if cash_in_hand_total else 0

    total_payments = member_loan_total + member_savings_return_total + bank_emi_total + bank_emi_interest_total + savings_account_payments_total + service_charge_payments_total + cash_in_hand_total


    print(total_payments, total_receipts)
    if total_payments > total_receipts:
        return jsonify({"meeting_status" : "Payments are more than Receipts; Wrong or Pending Entries", "status_class" : "text-danger"})
    elif total_payments < total_receipts:
        return jsonify({"meeting_status" : "Payments are less than Receipts; Pending Payment Entries", "status_class" : "text-danger"})
    else:
        if total_receipts != 0:
            return jsonify({"meeting_status" : "Payments and Receipts are Tallying Correctly!", "status_class" : "text-success"})
        else:
            return jsonify({"meeting_status" : "Meeting Entry Not Started", "status_class" : "text-danger"})
        
def internal_meeting_status(meeting_id):
    #Case 1 : Attendece and Member Receipts are not matching

    attendence = len(db.session.query(meetingAttendence).filter(meetingAttendence.meeting_id == meeting_id).all())
    # print(attendence)
    member_receipts = [r.member_id for r in db.session.query(memberSavingsReceipts.member_id).filter(memberSavingsReceipts.meeting_id == meeting_id).all() ]
    loan_repayment_receipts = [r.member_id for r in db.session.query(memberLoanRepaymentReceipts.member_id).filter(memberLoanRepaymentReceipts.meeting_id == meeting_id).all() ]
    receipts = set(member_receipts + loan_repayment_receipts)
    # print(member_receipts, loan_repayment_receipts)
    if len(receipts) != attendence:
        return {"meeting_status" : "Member receipts entry pending.", "status_class" : "text-danger"}
    
    #Case 2 : The Receipts total vs Payment Total is not matching
    
    # Member Receipts
    savings_total =  db.session.query(func.sum(memberSavingsReceipts.receipt_amount)).filter(memberSavingsReceipts.meeting_id == meeting_id).first()[0]
    savings_total = savings_total if savings_total else 0
    
    principal_total = db.session.query(func.sum(memberLoanRepaymentReceipts.principal_amount)).filter(memberLoanRepaymentReceipts.meeting_id == meeting_id).first()[0]
    principal_total = principal_total if principal_total else 0
    
    interest_total = db.session.query(func.sum(memberLoanRepaymentReceipts.interest_amount)).filter(memberLoanRepaymentReceipts.meeting_id == meeting_id).first()[0]
    interest_total = interest_total if interest_total else 0
    
    fine_total = db.session.query(func.sum(memberFineReceipts.receipt_amount)).filter(memberFineReceipts.meeting_id == meeting_id).first()[0]
    fine_total = fine_total if fine_total else 0
    # Other Receipts
    loan_receipts_total = db.session.query(func.sum(otherLoanReceipts.loan_amount)).filter(otherLoanReceipts.meeting_id == meeting_id).first()[0]
    loan_receipts_total = loan_receipts_total if loan_receipts_total else 0
    
    bank_saving_receipts_total = db.session.query(func.sum(otherSavingsReceipts.withdrawal_amount)).filter(otherSavingsReceipts.meeting_id == meeting_id).first()[0]
    bank_saving_receipts_total = bank_saving_receipts_total if bank_saving_receipts_total else 0

    total_receipts = savings_total + principal_total + interest_total + fine_total + loan_receipts_total + bank_saving_receipts_total

    # Member Payments
    member_loan_total = db.session.query(func.sum(memberLoanPayments.payment_amount)).filter(memberLoanPayments.meeting_id == meeting_id).first()[0]
    member_loan_total = member_loan_total if member_loan_total else 0
    
    member_savings_return_total = db.session.query(func.sum(memberSavingsPayments.payment_amount)).filter(memberSavingsPayments.meeting_id == meeting_id).first()[0]
    member_savings_return_total = member_savings_return_total if member_savings_return_total else 0
    # Other Payments

    bank_emi_total = db.session.query(func.sum(bankEmiPayments.principal_amount)).filter(bankEmiPayments.meeting_id == meeting_id).first()[0]
    bank_emi_total = bank_emi_total if bank_emi_total else 0
    
    bank_emi_interest_total = db.session.query(func.sum(bankEmiPayments.interest_amount)).filter(bankEmiPayments.meeting_id == meeting_id).first()[0]
    bank_emi_interest_total = bank_emi_interest_total if bank_emi_interest_total else 0
    
    savings_account_payments_total = db.session.query(func.sum(savingsAccountPayments.payment_amount)).filter(savingsAccountPayments.meeting_id == meeting_id).first()[0]
    savings_account_payments_total = savings_account_payments_total if savings_account_payments_total else 0
    
    service_charge_payments_total = db.session.query(func.sum(otherServiceChargePayments.payment_amount)).filter(otherServiceChargePayments.meeting_id == meeting_id).first()[0]
    service_charge_payments_total = service_charge_payments_total if service_charge_payments_total else 0
    
    cash_in_hand_total = db.session.query(func.sum(otherCashInHandPayments.payment_amount)).filter(otherCashInHandPayments.meeting_id == meeting_id).first()[0]
    cash_in_hand_total = cash_in_hand_total if cash_in_hand_total else 0

    total_payments = member_loan_total + member_savings_return_total + bank_emi_total + bank_emi_interest_total + savings_account_payments_total + service_charge_payments_total + cash_in_hand_total


    # print(total_payments, total_receipts)
    if total_payments > total_receipts:
        return {"meeting_status" : "Payments are more than Receipts; Wrong or Pending Entries", "status_class" : "text-danger"}
    elif total_payments < total_receipts:
        return {"meeting_status" : "Payments are less than Receipts; Pending Payment Entries", "status_class" : "text-danger"}
    else:
        if total_receipts != 0:
            return {"meeting_status" : "Entry Completed. Everything is tallying.", "status_class" : "text-success"}
        else:
            return {"meeting_status" : "Meeting Entry Not Started", "status_class" : "text-danger"}
        
@app.route("/shareoutReport/<int:shg_id>")
@auth_required('token')
@roles_required('operator')
def shareoutReport(shg_id):
    f_date = db.session.query(SHG.formation_date).filter(SHG.id == shg_id).first()[0]

    current_date = datetime.today()

    diff = current_date.date() - f_date

    if ( diff < timedelta(weeks=52)):
        return jsonify(False)
    else:
        data = [
            {
                "name" : "Name", 
                "savings" : "Savings",
                "loan_outstanding" : "Loan Outstanding",
                "interest_outstanding": "Interest Outstanding", 
                "Difference" : "Difference", 
                "Amount Payble": "Amount Payble",
                "Amount Receivable": "Amount Receivable"
            }
        ]

        members = db.session.query(Member).filter(Member.shg_id == shg_id).all()

        return jsonify(data)



#route all unreconignized routes to /
@app.route('/<path:path>')
def all(path):
    return "<h1>It Seems that you are accessing the URL manually. For security reason this has been blocked. <a href='/'>Click here to Go Home</a></h1>"


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
    
    member_receipts = [r.member_id for r in db.session.query(memberSavingsReceipts.member_id).filter(memberSavingsReceipts.meeting_id == meeting_id).all() ]
    loan_repayment_receipts = [r.member_id for r in db.session.query(memberLoanRepaymentReceipts.member_id).filter(memberLoanRepaymentReceipts.meeting_id == meeting_id).all() ]
    receipts = set(member_receipts + loan_repayment_receipts)

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
    
    # bank_emi_interest_total = db.session.query(func.sum(bankEmiPayments.interest_amount)).filter(bankEmiPayments.meeting_id == meeting_id).first()[0]
    # bank_emi_interest_total = bank_emi_interest_total if bank_emi_interest_total else 0
    
    savings_account_payments_total = db.session.query(func.sum(savingsAccountPayments.payment_amount)).filter(savingsAccountPayments.meeting_id == meeting_id).first()[0]
    savings_account_payments_total = savings_account_payments_total if savings_account_payments_total else 0
    
    service_charge_payments_total = db.session.query(func.sum(otherServiceChargePayments.payment_amount)).filter(otherServiceChargePayments.meeting_id == meeting_id).first()[0]
    service_charge_payments_total = service_charge_payments_total if service_charge_payments_total else 0
    
    cash_in_hand_total = db.session.query(func.sum(otherCashInBoxPayments.payment_amount)).filter(otherCashInBoxPayments.meeting_id == meeting_id).first()[0]
    cash_in_hand_total = cash_in_hand_total if cash_in_hand_total else 0

    total_payments = member_loan_total + member_savings_return_total + bank_emi_total + savings_account_payments_total + service_charge_payments_total + cash_in_hand_total


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
    
    # bank_emi_interest_total = db.session.query(func.sum(bankEmiPayments.interest_amount)).filter(bankEmiPayments.meeting_id == meeting_id).first()[0]
    # bank_emi_interest_total = bank_emi_interest_total if bank_emi_interest_total else 0
    
    savings_account_payments_total = db.session.query(func.sum(savingsAccountPayments.payment_amount)).filter(savingsAccountPayments.meeting_id == meeting_id).first()[0]
    savings_account_payments_total = savings_account_payments_total if savings_account_payments_total else 0
    
    service_charge_payments_total = db.session.query(func.sum(otherServiceChargePayments.payment_amount)).filter(otherServiceChargePayments.meeting_id == meeting_id).first()[0]
    service_charge_payments_total = service_charge_payments_total if service_charge_payments_total else 0
    
    cash_in_hand_total = db.session.query(func.sum(otherCashInBoxPayments.payment_amount)).filter(otherCashInBoxPayments.meeting_id == meeting_id).first()[0]
    cash_in_hand_total = cash_in_hand_total if cash_in_hand_total else 0

    total_payments = member_loan_total + member_savings_return_total + bank_emi_total + savings_account_payments_total + service_charge_payments_total + cash_in_hand_total


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
        


#route all unreconignized routes to /
@app.route('/<path:path>')
def all(path):
    return "<h1>It Seems that you are accessing the URL manually. For security reason this has been blocked. <a href='/'>Click here to Go Home</a></h1>"

@app.route("/savingsReport/byMonth/<int:month>")
def savingsReportByMonth(month):
    
    # Sr No | Shg Name | Expected Atttnedence | Actual Attendece | Expected Savings | Actual Savings | Number of Non savers |
    mets = db.session.query(meetings).filter(func.strftime('%m', meetings.meeting_date) == f'{month:02d}').all()
    data = []
    for meeting in mets:
        name = db.session.query(SHG.shg_name).filter(SHG.id == meeting.shg_id).first()[0]
        expected_attendence = db.session.query(members.shg_id).filter(members.shg_id == meeting.shg_id, members.active == 1).count()
        # meeting_id = db.session.query(meetings.id).filter(meetings.shg_id == shg.id, func.strftime('%m', meetings.meeting_date) == f'{month:02d}').first()
        actual_attendence = db.session.query(meetingAttendence).filter(meetingAttendence.meeting_id == meeting.id, meetingAttendence.attended == 1).count() 
        expected_savings = expected_attendence * db.session.query(SHG.per_share_size_in_INR).filter(SHG.id == meeting.shg_id).first()[0] * 5
        actual_savings = db.session.query(func.sum(memberSavingsReceipts.receipt_amount)).filter(memberSavingsReceipts.meeting_id == meeting.id).first()[0]
        number_of_non_savers = actual_attendence - db.session.query(func.count(memberSavingsReceipts.receipt_amount)).filter(memberSavingsReceipts.meeting_id == meeting.id).first()[0] 

        data.append({
            "name" : name,
            "meeting_date" : datetime.strftime(meeting.meeting_date, "%d-%b-%Y"),
            "expected_attendence" : expected_attendence,
            "actual_attendence" : actual_attendence,
            "expected_savings" : expected_savings,
            "actual_savings" : actual_savings,
            "number_of_non_savers" : number_of_non_savers
        })
    return jsonify(data)

@app.route("/share_price/<int:meeting_id>")
def share_price(meeting_id):
    shg_id = db.session.query(meetings.shg_id).filter(meetings.id == meeting_id).first()[0]
    share_price = db.session.query(SHG.per_share_size_in_INR).filter(SHG.id == shg_id).first()[0]
    return jsonify(share_price)

@app.route("/shareout_report/<int:group_id>")
def shareout_report(group_id):
    # total_money = Member_Loan_OS + Cash at bank & cash at box

    members_list = db.session.query(members).filter(members.shg_id == group_id).all()


    share_price = db.session.query(SHG.per_share_size_in_INR).filter(SHG.id == group_id).first()[0]
    cash_in_box = db.session.query(SHG.cash_in_box).filter(SHG.id == group_id).first()[0]
    cash_at_bank = db.session.query(func.sum(shgBankAccount.balance)).filter(shgBankAccount.shg_id == group_id).filter(shgBankAccount.account_type == "savings").first()[0]
    bank_loan_outstanding = db.session.query(func.sum(shgBankAccount.balance)).filter(shgBankAccount.shg_id == group_id).filter(shgBankAccount.account_type == "loan").first()[0]
    
    member_loan_outstanding = 0
    member_interest_outstanding = 0 
    total_member_savings = 0
    for member in members_list:
        member_loan_outstanding += member.loan_outstanding
        member_interest_outstanding += member.interest_outstanding
        total_member_savings += member.total_savings

    total_number_of_shares = total_member_savings // share_price


    total_amount = cash_at_bank + cash_in_box + member_loan_outstanding + member_interest_outstanding
    paybale = bank_loan_outstanding

    net_profit = total_amount - paybale - total_member_savings
    net_profit_per_share = net_profit / total_number_of_shares

    final_data = [{"shg": {}, "members":[]}]

    final_data[0]["shg"] = {
        "name" : db.session.query(SHG.shg_name).filter(SHG.id == group_id).first()[0],
        "total_number_of_shares" : total_number_of_shares,
        "total_member_savings" : total_member_savings,
        "bank_loan_outstanding" : bank_loan_outstanding,
        "total_amount" : total_amount,
        "paybale" : paybale,
        "net_profit" : net_profit
    }
    for member in members_list:
        final_data[0]["members"].append({

            "name" : member.first_name + " " + member.father_husband_name + " " + member.last_name,
            "total_savings" : member.total_savings,
            "member_loan_outstanding" : member.loan_outstanding,
            "member_interest_outstanding" : member.interest_outstanding,
            "savings_after_loan" : member.total_savings - member.loan_outstanding - member.interest_outstanding,
            "profit" : (member.total_savings // share_price) * net_profit_per_share

        })

    return jsonify(final_data)
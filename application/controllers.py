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

    cash_in_hand_receipts_total = db.session.query(func.sum(otherCashInBoxReceipts.receipt_amount)).filter(otherCashInBoxReceipts.meeting_id == meeting_id).first()[0]
    cash_in_hand_receipts_total = cash_in_hand_receipts_total if cash_in_hand_receipts_total else 0

    total_receipts = savings_total + principal_total + interest_total + fine_total + loan_receipts_total + bank_saving_receipts_total + cash_in_hand_receipts_total

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

    total_member_receipts = savings_total + principal_total + interest_total + fine_total
    total_member_receipts = total_member_receipts if total_member_receipts else 0
    total_other_receipts = loan_receipts_total + bank_saving_receipts_total + cash_in_hand_receipts_total
    total_other_receipts = total_other_receipts if total_other_receipts else 0

    total_member_payments = member_loan_total + member_savings_return_total
    total_member_payments = total_member_payments if total_member_payments else 0
    total_other_payments = bank_emi_total + savings_account_payments_total + service_charge_payments_total + cash_in_hand_total
    total_other_payments = total_other_payments if total_other_payments else 0

    first_half = {"total_member_receipts" : total_member_receipts, "total_other_receipts" : total_other_receipts, "total_member_payments" : total_member_payments, "total_other_payments" : total_other_payments}
    
    if len(receipts) != attendence:
        first_half.update({"meeting_status" : "Member receipts entry pending", "status_class" : "text-danger"})
    
    elif total_payments > total_receipts:
        first_half.update({"meeting_status" : "Payments are more than Receipts; Wrong or Pending Entries", "status_class" : "text-danger"})
    elif total_payments < total_receipts:
        first_half.update({"meeting_status" : "Payments are less than Receipts; Pending Payment Entries", "status_class" : "text-danger"})
    else:
        if total_receipts != 0:
            first_half.update({"meeting_status" : "Payments and Receipts are Tallying Correctly!", "status_class" : "text-success"})
        else:
            first_half.update({"meeting_status" : "Meeting Entry Not Started", "status_class" : "text-danger"})
    
    return jsonify(first_half) #first_half

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
    time.sleep(10)
    data = []
    shgs = db.session.query(SHG).all()

    if not shgs:
        return jsonify("No Data Found")
    days = {
        1: "Monday",
        2: "Tuesday",
        3: "Wednesday",
        4: "Thursday",
        5: "Friday",
        6: "Saturday",
        7: "Sunday"
    }
    counter = 1
    for shg in shgs:
        row = {
            'sn': None,
            'group_name': None,
            'district': None,
            'block': None,
            'panchayat': None,
            'village': None,
            'tola': None,
            'ward_no': None,
            'min': None,
            'gen': None,
            'sc': None,
            'obc': None,
            'total_member': None,
            'first_training_meeting_date': None,
            'saving_starting_date_of_the_cycle': None,
            'share_out_date': None,
            'meeting_day': None,
            'meeting_time': None,
            'name_of_group_leader': None,
            'mobile_no': None,
            'stamp_value_of_the_cycle_(rs)': None,
            'monthly_loan_meeting_date': None,
            'present_total_member_in_the_loan_meeting': None,
            'no_of_total_share_for_this_month': None,
            'cumulative_saving_till_previous_month': None,
            'saving_for_the_month': None,
            'cumulative_savings_of_this_cycle_rs': None,
            'no_of_loans_outstanding_till_previous_month': None,
            'cumulative_loan_amount_till_previous_month': None,
            'no_of_loan_for_the_month': None,
            'loan_amount_for_the_month': None,
            'total_no_of_loan_till_this_month': None,
            'lone_reseved_in_this_lon_meatting': None,
            'value_of_loan_repaid_(interest)': None,
            'value_of_loans_outstanding_rs': None,
            'loan_fund:_cash_in_box_(rs)': None,
            'bank_account_openend__(y/n)': None,
            'loan_fund:_cash_in_bank_(rs)': None,
            'bank_account_date': None,
            'bank_account_no': None,
            'name_of_the_bank': None,
            'branch': None,
            'no_of_bpl': None,
            'date_submitted': None,
            'name_of_crp': None
        }
        
        
        row['sn'] = counter
        row['group_name'] = shg.shg_name
        row['district'] = ""
        row['block'] = ""
        row['panchayat'] = ""
        row['village'] = shg.village_name
        row['tola'] = ""
        row['ward_no'] = ""
        row['min'] = ""
        row['gen'] = db.session.query(members).filter(members.shg_id == shg.id, members.active == 1, members.category == 'General').count()
        row['sc'] = db.session.query(members).filter(members.shg_id == shg.id, members.active == 1, members.category == 'SC').count()
        row['obc'] = db.session.query(members).filter(members.shg_id == shg.id, members.active == 1, members.category == 'OBC').count()
        row['total_member'] = db.session.query(members).filter(members.shg_id == shg.id, members.active == 1).count()
        row['first_training_meeting_date'] = shg.formation_date
        row['saving_starting_date_of_the_cycle'] = shg.first_saving_date
        row['share_out_date'] = shg.formation_date + timedelta(weeks=52)
        row['meeting_day'] = days[shg.saving_day]
        row['meeting_time'] = ""
        row['name_of_group_leader'] = ""
        row['mobile_no'] = ""
        row['stamp_value_of_the_cycle_rs'] = shg.per_share_size_in_INR
        row['monthly_loan_meeting_date'] = ""
        print(shg.id , f'{month:02d}')
        meeting = db.session.query(meetings).filter(meetings.shg_id == shg.id, func.strftime('%m', meetings.meeting_date) == f'{month:02d}').first()
        
        row['present_total_member_in_the_loan_meeting'] = meeting.attendece if meeting else 0
        row['no_of_total_share_for_this_month'] = int(db.session.query(func.sum(memberSavingsReceipts.receipt_amount)).filter(memberSavingsReceipts.meeting_id == meeting.id).first()[0] / shg.per_share_size_in_INR) if meeting else 0
        
        if meeting:
            row['cumulative_saving_till_previous_month'] = db.session.query(func.sum(memberSavingsReceipts.receipt_amount)).filter(memberSavingsReceipts.meeting_id.in_(db.session.query(meetings.id).filter(meetings.shg_id == shg.id, meetings.meeting_date < meeting.meeting_date).all())).scalar()
        else:
            row['cumulative_saving_till_previous_month'] = 0
        row['saving_for_the_month'] = db.session.query(func.sum(memberSavingsReceipts.receipt_amount)).filter(memberSavingsReceipts.meeting_id == meeting.id).first()[0] if meeting else 0

        row['cumulative_savings_of_this_cycle_rs'] = row['cumulative_saving_till_previous_month'] + row['saving_for_the_month'] if row['cumulative_saving_till_previous_month'] else row['saving_for_the_month']

        row['no_of_loans_outstanding_till_previous_month'] = db.session.query(members).filter(members.shg_id == shg.id, members.active == 1, members.loan_outstanding > 0).count()

        row['cumulative_loan_amount_till_previous_month'] = db.session.query(func.sum(members.loan_outstanding)).filter(members.shg_id == shg.id,).first()[0]

        row['no_of_loan_for_the_month'] = db.session.query(memberLoanPayments).filter(memberLoanPayments.meeting_id == meeting.id, func.strftime('%m', memberLoanPayments.payment_date) == f'{month:02d}').count()  if meeting else 0 # db.session.query(memberLoanPayments).filter(memberLoanPayments.meeting_id == meeting.id, memberLoanPayments.payment_date ).count()
    
        row['loan_amount_for_the_month'] = db.session.query(func.sum(memberLoanPayments.payment_amount)).filter(memberLoanPayments.meeting_id == meeting.id, func.strftime('%m', memberLoanPayments.payment_date) == f'{month:02d}').count()  if meeting else 0

        row['total_no_of_loan_till_this_month'] =  row['no_of_loans_outstanding_till_previous_month']

        row['lone_reseved_in_this_lon_meatting'] =  db.session.query(func.sum(memberLoanRepaymentReceipts.principal_amount)).filter(memberLoanRepaymentReceipts.meeting_id == meeting.id, func.strftime('%m', memberLoanRepaymentReceipts.receipt_date) == f'{month:02d}').first()[0] if meeting else 0

        row['value_of_loan_repaid_interest'] = db.session.query(func.sum(memberLoanRepaymentReceipts.interest_amount)).filter(memberLoanRepaymentReceipts.meeting_id == meeting.id, func.strftime('%m', memberLoanRepaymentReceipts.receipt_date) == f'{month:02d}').first()[0] if meeting else 0

        row["value_of_loans_outstanding_rs"] = row["cumulative_loan_amount_till_previous_month"] + row['loan_amount_for_the_month'] - row['lone_reseved_in_this_lon_meatting'] if row["cumulative_loan_amount_till_previous_month"] and row["lone_reseved_in_this_lon_meatting"] else row['loan_amount_for_the_month']

        row['loan_fund_cash_in_bank_rs'] = shg.cash_in_box

        savings_account = db.session.query(shgBankAccount).filter(shgBankAccount.shg_id == shg.id, shgBankAccount.account_type == 'savings').first()
        
        row["bank_account_openend__y_n"] = "Yes" if savings_account else "No"

        row['loan_fund_cash_in_bank_rs'] = savings_account.balance if savings_account else 0

        row["bank_account_date"] = 'N/A'

        row['bank_account_no'] = savings_account.account_number if savings_account else 'N/A'

        row["name_of_the_bank"] = savings_account.bank_name if savings_account else 'N/A'

        row["branch"] = savings_account.branch if savings_account else 'N/A'

        row["no_of_bpl"] = "N/A"

        row["date_submitted"] = "N/A"

        row["name_of_crp"] = shg.samuh_sakhi_name
 
        data.append(row)
        counter += 1

    return jsonify(data)





    # Sr No | Shg Name | Expected Atttnedence | Actual Attendece | Expected Savings | Actual Savings | Number of Non savers |
    # mets = db.session.query(meetings).filter(func.strftime('%m', meetings.meeting_date) == f'{month:02d}').all()
    # data = []
    # for meeting in mets:
    #     name = db.session.query(SHG.shg_name).filter(SHG.id == meeting.shg_id).first()[0]
    #     expected_attendence = db.session.query(members.shg_id).filter(members.shg_id == meeting.shg_id, members.active == 1).count()
    #     # meeting_id = db.session.query(meetings.id).filter(meetings.shg_id == shg.id, func.strftime('%m', meetings.meeting_date) == f'{month:02d}').first()
    #     actual_attendence = db.session.query(meetingAttendence).filter(meetingAttendence.meeting_id == meeting.id, meetingAttendence.attended == 1).count() 
    #     expected_savings = expected_attendence * db.session.query(SHG.per_share_size_in_INR).filter(SHG.id == meeting.shg_id).first()[0] * 5
    #     actual_savings = db.session.query(func.sum(memberSavingsReceipts.receipt_amount)).filter(memberSavingsReceipts.meeting_id == meeting.id).first()[0]
    #     number_of_non_savers = actual_attendence - db.session.query(func.count(memberSavingsReceipts.receipt_amount)).filter(memberSavingsReceipts.meeting_id == meeting.id).first()[0] 

    #     data.append({
    #         "name" : name,
    #         "meeting_date" : datetime.strftime(meeting.meeting_date, "%d-%b-%Y"),
    #         "expected_attendence" : expected_attendence,
    #         "actual_attendence" : actual_attendence,
    #         "expected_savings" : expected_savings,
    #         "actual_savings" : actual_savings,
    #         "number_of_non_savers" : number_of_non_savers
    #     })
    # return jsonify(data)

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
    print("total_amount" , total_amount, "cast_at_bank", cash_at_bank, "cash_in_box", cash_in_box, "member_loan_outstanding", member_loan_outstanding, "member_interest_outstanding", member_interest_outstanding)
    payable = bank_loan_outstanding

    net_profit = total_amount - payable - total_member_savings

    print("cash in box", cash_in_box,
        "\ncash at bank", cash_at_bank, 
        "\nmember loan outstanding", member_loan_outstanding,
        "\nmember interest outstanding", member_interest_outstanding,
        "\ntotal member savings", total_member_savings,
        "\nbank loan outstanding", bank_loan_outstanding,
        "\nnet profit", net_profit)
    net_profit_per_share = net_profit / total_number_of_shares

    final_data = [{"shg": {}, "members":[]}]

    final_data[0]["shg"] = {
        "name" : db.session.query(SHG.shg_name).filter(SHG.id == group_id).first()[0],
        "total_number_of_shares" : total_number_of_shares,
        "total_member_savings" : total_member_savings,
        "bank_loan_outstanding" : bank_loan_outstanding,
        "total_amount" : total_amount,
        "payable" : payable,
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
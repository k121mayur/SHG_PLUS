from application.database import db
from flask_security import UserMixin, RoleMixin
from sqlalchemy import event
from sqlalchemy.orm.attributes import set_committed_value
from sqlalchemy import Numeric

class Users(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, autoincrement=True, nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    # role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    password = db.Column(db.String(80), nullable=False)
    roles = db.relationship('Roles', secondary='roles_users', backref=db.backref('users', lazy='dynamic'))
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    last_login = db.Column(db.DateTime, nullable=False)
    active = db.Column(db.Boolean)
    date_created = db.Column(db.DateTime, nullable=False)


class Roles(db.Model, RoleMixin):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(80), nullable=False)

class RolesUsers(db.Model):
    __tablename__ = 'roles_users'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
    role_id = db.Column('role_id', db.Integer, db.ForeignKey('roles.id'))


class staff(db.Model):
    __tablename__ = 'staff'
    id = db.Column(db.Integer, primary_key=True)
    staff_name = db.Column(db.String(80), nullable=False)
    # Will add this details as required


class SHG(db.Model):
    __tablename__ = 'shg'
    id = db.Column(db.Integer, primary_key=True)
    shg_name = db.Column(db.String(80), nullable=False)
    project_name = db.Column(db.String(50), nullable=False)
    village_name = db.Column(db.String(50), nullable=False)
    panchayat_name = db.Column(db.String(50), nullable=False)
    group_address = db.Column(db.Text, nullable=False)
    formation_date = db.Column(db.Date, nullable=False)
    first_saving_date = db.Column(db.Date, nullable=False)

    total_no_of_members = db.Column(db.Integer, nullable=False)
    saving_day = db.Column(db.Integer, nullable=False)
    staff_name = db.Column(db.String(80), nullable=False)
    samuh_sakhi_name = db.Column(db.String(80), nullable=False)
    per_share_size_in_INR = db.Column(db.Integer, nullable=False)
    
    active = db.Column(db.Boolean, nullable=False, default=True)


class shgBankAccount(db.Model):
    __tablename__ = 'shgBankAccount'
    id = db.Column(db.Integer, primary_key=True)
    account_type = db.Column(db.String(10), nullable=False)
    bank_name = db.Column(db.String(100), nullable=False)
    branch = db.Column(db.String(100), nullable=False)
    account_name = db.Column(db.String(100), nullable=False)
    account_number = db.Column(db.String(50), nullable=False)
    IFSC_code = db.Column(db.String(20), nullable=False)
    shg_id = db.Column(db.Integer, db.ForeignKey('shg.id'), nullable=False)
    balance = db.Column(db.Integer, nullable=False, default=0)


class schemes(db.Model):
    __tablename__ = 'schemes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    scheme_name = db.Column(db.String(80), nullable=False)

class members(db.Model):
    __tablename__ = 'members'

    member_id = db.Column(db.Integer, primary_key=True)
    shg_id = db.Column(db.Integer, nullable=False)

    joining_date = db.Column(db.Date, nullable=False)

    village = db.Column(db.String(50))
    household_code = db.Column(db.String(20), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    father_husband_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    number_of_family_members = db.Column(db.Integer, nullable=False)
    voter_id = db.Column(db.String(20))
    adhar_id = db.Column(db.String(20))
    pan_number = db.Column(db.String(20))
    ration_card_number = db.Column(db.String(20))
    education = db.Column(db.String(40), nullable=False)
    category = db.Column(db.String(20))
    caste = db.Column(db.String(20))
    number_of_family_members = db.Column(db.Integer, nullable=False)
    mobile_number = db.Column(db.Integer, nullable=False)
    total_land_kattha = db.Column(Numeric(precision=10, scale=2))
    total_irrigated_land_kattha = db.Column(db.Integer)
    total_no_of_goats = db.Column(db.Integer)
    total_no_of_cattle = db.Column(db.Integer)
    total_no_of_members_migrated = db.Column(db.Integer)
    main_source_of_income = db.Column(db.String(50))
    head_of_the_family_name = db.Column(db.String(50))
    
    total_savings = db.Column(db.Integer, default=0)
    loan_outstanding = db.Column(db.Integer, default=0)
    interest_outstanding = db.Column(db.Integer, default=0)

    active = db.Column(db.Boolean, default=True)

class schemeMemberEnrollment(db.Model):
    __tablename__ = 'schemeMemberEnrollment'
    id = db.Column(db.Integer, autoincrement = True)
    member_id = db.Column(db.Integer, db.ForeignKey('members.member_id'), nullable=False, primary_key=True)
    scheme_id = db.Column(db.Integer, db.ForeignKey('schemes.id'), nullable=False, primary_key=True)
    __table_args__ = (db.UniqueConstraint('member_id', 'scheme_id'),)

class memberBankAccount(db.Model):
    __tablename__ = 'memberBankAccount'
    id = db.Column(db.Integer, primary_key=True)
    account_type = db.Column(db.String(10), nullable=False)
    bank_name = db.Column(db.String(20), nullable=False)
    branch = db.Column(db.String(20), nullable=False)
    account_name = db.Column(db.String(30), nullable=False)
    account_number = db.Column(db.String(20), nullable=False)
    IFSC_code = db.Column(db.String(11), nullable=False)
    member_id = db.Column(db.Integer, db.ForeignKey('members.member_id'), nullable=False)
    __table_args__ = (db.UniqueConstraint('member_id', 'account_number'),)

class meetings(db.Model):
    __tablename__ = 'meetings'
    id = db.Column(db.Integer, primary_key=True)
    shg_id = db.Column(db.Integer, db.ForeignKey('shg.id'), nullable=False)
    meeting_date = db.Column(db.Date, nullable=False)
    attendece = db.Column(db.Integer, nullable=False)
    conducted = db.Column(db.Boolean, nullable=False)
    __table_args__ = (db.UniqueConstraint('shg_id', 'meeting_date'),)

class meetingAttendence(db.Model):
    __tablename__ = 'meetingAttendence'
    id = db.Column(db.Integer, primary_key=True)
    meeting_id = db.Column(db.Integer, db.ForeignKey('meetings.id'), nullable=False)
    member_id = db.Column(db.Integer, db.ForeignKey('members.member_id'), nullable=False)
    attended = db.Column(db.Boolean, nullable=False)
    __table_args__ = (db.UniqueConstraint('member_id', 'meeting_id'),)

class memberSavingsReceipts(db.Model):
    __tablename__ = 'memberSavingsReceipts'
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('members.member_id'), nullable=False)
    meeting_id = db.Column(db.Integer, db.ForeignKey('meetings.id'), nullable=False)
    receipt_date = db.Column(db.Date, nullable=False)
    receipt_amount = db.Column(db.Integer, nullable=False)
    __table_args__ = (db.UniqueConstraint('member_id', 'meeting_id'),)

    
     # Add here event listener to add savings to the member's total savings when a receipt is made

class memberLoanRepaymentReceipts(db.Model):
    __tablename__ = 'memberLoanRepaymentReceipts'
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('members.member_id'), nullable=False)
    meeting_id = db.Column(db.Integer, db.ForeignKey('meetings.id'), nullable=False)
    receipt_date = db.Column(db.Date, nullable=False)
    principal_amount = db.Column(db.Integer, nullable=False)
    interest_amount = db.Column(db.Integer, nullable=False)

    # member_loan_id = db.column(db.Integer, db.ForeignKey('memberLoanPayments.id'), nullable=False)
    
    # Add Event listener here to reduce loan outstanding when a receipt is made
   
class memberFineReceipts(db.Model):
    __tablename__ = 'memberFineReceipts'
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('members.member_id'), nullable=False)
    meeting_id = db.Column(db.Integer, db.ForeignKey('meetings.id'), nullable=False)
    receipt_date = db.Column(db.Date, nullable=True) # Receipt date currently I feel optional let us see if we need it
    receipt_amount = db.Column(db.Integer, nullable=False)

class otherLoanReceipts(db.Model):
    __tablename__ = 'otherLoanReceipts'
    id = db.Column(db.Integer, primary_key=True)
    meeting_id = db.Column(db.Integer, db.ForeignKey('meetings.id'), nullable=False)

    loan_account_id = db.Column(db.Integer, db.ForeignKey('shgBankAccount.id'), nullable=False )
    loan_amount = db.Column(db.Integer, nullable=False)
    loan_tenure = db.Column(db.Integer, nullable=False)
    loan_date = db.Column(db.Date, nullable=False)
    loan_type = db.Column(db.String(20), nullable=False)
    loan_interest_rate = db.Column(db.Integer, nullable=False)
    __table_args__ = (db.UniqueConstraint('loan_account_id', 'meeting_id'),)

class otherSavingsReceipts(db.Model):
    __tablename__ = 'otherSavingsReceipts'
    id = db.Column(db.Integer, primary_key=True)
    meeting_id = db.Column(db.Integer, db.ForeignKey('meetings.id'), nullable=False)
    savings_account_id = db.Column(db.Integer, db.ForeignKey('shgBankAccount.id'), nullable=True)
    withdrawal_date = db.Column(db.Date, nullable=True)
    withdrawal_amount = db.Column(db.Integer, nullable=True)
    __table_args__ = (db.UniqueConstraint('savings_account_id', 'meeting_id'),)

class otherCashInHandReceipts(db.Model):
    __tablename__ = 'otherCashInHandReceipts'
    id = db.Column(db.Integer, primary_key=True)
    meeting_id = db.Column(db.Integer, db.ForeignKey('meetings.id'), nullable=False)
    member_id = db.Column(db.Integer, db.ForeignKey('members.member_id'), nullable=False)
    receipt_date = db.Column(db.Date, nullable=False)
    receipt_amount = db.Column(db.Integer, nullable=False)
    __table_args__ = (db.UniqueConstraint('member_id', 'meeting_id'),)


class loanPurposeList(db.Model):
    __tablename__ = 'loanPurposeList'
    id = db.Column(db.Integer, primary_key=True)
    loan_type_id = db.Column(db.Integer, nullable=False)
    loan_purpose = db.Column(db.String(20), nullable=False)


class memberLoanPayments(db.Model):
    __tablename__ = 'memberLoanPayments'
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('members.member_id'), nullable=False)
    meeting_id = db.Column(db.Integer, db.ForeignKey('meetings.id'), nullable=False)
    payment_date = db.Column(db.Date, nullable=False)
    payment_amount = db.Column(db.Integer, nullable=False)
    loan_purpose = db.Column(db.Integer, db.ForeignKey('loanPurposeList.id'), nullable=False)
    __table_args__ = (db.UniqueConstraint('meeting_id', 'member_id'),)


class memberSavingsPayments(db.Model):
    __tablename__ = 'memberSavingsPayments'
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('members.member_id'), nullable=False)
    meeting_id = db.Column(db.Integer, db.ForeignKey('meetings.id'), nullable=False)
    payment_date = db.Column(db.Date, nullable=False)
    reason = db.Column(db.String(50), nullable=False)
    payment_amount = db.Column(db.Integer, nullable=False)
    __table_args__ = (db.UniqueConstraint('meeting_id', 'member_id'),)


class bankEmiPayments(db.Model):
    __tablename__ = 'bankEmiPayments'
    id = db.Column(db.Integer, primary_key=True)
    meeting_id = db.Column(db.Integer, db.ForeignKey('meetings.id'), nullable=False)
    loan_account_id = db.Column(db.Integer, db.ForeignKey('shgBankAccount.id'), nullable=False)
    payment_date = db.Column(db.Date, nullable=False)
    principal_amount = db.Column(db.Integer, nullable=False)
    interest_amount = db.Column(db.String(20), nullable=False)
    __table_args__ = (db.UniqueConstraint('meeting_id', 'loan_account_id'),)


class savingsAccountPayments(db.Model):
    __tablename__ = 'savingsAccountPayment'
    id = db.Column(db.Integer, primary_key=True)
    meeting_id = db.Column(db.Integer, db.ForeignKey('meetings.id'), nullable=False)
    savings_account_id = db.Column(db.Integer, db.ForeignKey('shgBankAccount.id'), nullable=False)
    payment_date = db.Column(db.Date, nullable=False)
    payment_amount = db.Column(db.Integer, nullable=False)


class otherServiceChargePayments(db.Model):
    __tablename__ = 'otherServiceChargePayments'
    id = db.Column(db.Integer, primary_key=True)
    meeting_id = db.Column(db.Integer, db.ForeignKey('meetings.id'), nullable=False)    
    payment_date = db.Column(db.Date, nullable=False)    
    payment_amount = db.Column(db.Integer, nullable=False)
    member_id = db.Column(db.Integer, db.ForeignKey('members.member_id'), nullable=False)


class otherCashInHandPayments(db.Model):
    __tablename__ = 'otherCashInHandPayments'
    id = db.Column(db.Integer, primary_key=True)
    meeting_id = db.Column(db.Integer, db.ForeignKey('meetings.id'), nullable=False)
    payment_date = db.Column(db.Date, nullable=False)
    payment_amount = db.Column(db.Integer, nullable=False)
    member_id = db.Column(db.Integer, db.ForeignKey('members.member_id'), nullable=False) # Bank Emi / Interest / Travelling / etc


class shgBankLoan(db.Model):
    __tablename__ = 'shgBankLoan'
    id = db.Column(db.Integer, primary_key=True)
    loan_account_id = db.Column(db.Integer, db.ForeignKey('shgBankAccount.id'), nullable=False)
    loan_amount = db.Column(db.Integer, nullable=False)
    loan_type = db.Column(db.String(20), nullable=False)
    loan_tenure = db.Column(db.Integer, nullable=False)
    loan_date = db.Column(db.Date, nullable=False)
    shg_id = db.Column(db.Integer, db.ForeignKey('shg.id'), nullable=False)
    balance = db.Column(db.Integer, nullable=False)


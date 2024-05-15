from application.database import db
from flask_security import UserMixin, RoleMixin


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


class SHG(db.Model):
    __tablename__ = 'shg'
    id = db.Column(db.Integer, primary_key=True)
    shg_name = db.Column(db.String(80), nullable=False)
    project_name = db.Column(db.String(100), nullable=False)
    village_name = db.Column(db.String(100), nullable=False)
    panchayat_name = db.Column(db.String(100), nullable=False)
    group_address = db.Column(db.Text, nullable=False)
    formation_date = db.Column(db.Date, nullable=False)
    total_no_of_members = db.Column(db.Integer, nullable=False)
    saving_day = db.Column(db.Integer, nullable=False)
    place_of_meeting = db.Column(db.String(100), nullable=False)
    staff_name = db.Column(db.String(80), nullable=False)
    samuh_sakhi_name = db.Column(db.String(80), nullable=False)
    per_share_size_in_INR = db.Column(db.Integer, nullable=False)


class shgBankAccount(db.Model):
    __tablename__ = 'shg_bank_account'
    id = db.Column(db.Integer, primary_key=True)
    account_type = db.Column(db.String(10), nullable=False)
    bank_name = db.Column(db.String(100), nullable=False)
    branch = db.Column(db.String(100), nullable=False)
    account_name = db.Column(db.String(100), nullable=False)
    account_number = db.Column(db.String(50), nullable=False)
    IFSC_code = db.Column(db.String(20), nullable=False)
    shg_id = db.Column(db.Integer, db.ForeignKey('shg.id'), nullable=False)


class  members(db.Model):
    __tablename__ = 'members'

    member_id = db.Column(db.Integer, primary_key=True)
    shg_id = db.Column(db.Integer, nullable=False)
    village = db.Column(db.String(255))
    household_code = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(255), nullable=False)
    father_husband_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    number_of_family_members = db.Column(db.Integer)
    voter_id = db.Column(db.String(255))
    adhar_id = db.Column(db.String(255))
    pan_number = db.Column(db.String(255))
    ration_card_number = db.Column(db.String(255))
    education = db.Column(db.String(255))
    category = db.Column(db.String(255))
    caste = db.Column(db.String(255))
    mobile_number = db.Column(db.String(10), nullable=False)
    total_land_kattha = db.Column(db.Integer)
    total_irrigated_land_kattha = db.Column(db.Integer)
    total_no_of_goats = db.Column(db.Integer)
    total_no_of_cattle = db.Column(db.Integer)
    total_no_of_members_migrated = db.Column(db.Integer)
    main_source_of_income = db.Column(db.String(255))
    head_of_the_family_name = db.Column(db.String(255))
    total_savings = db.Column(db.Integer)
    loan_outstanding = db.Column(db.Integer)
    interest_outstanding = db.Column(db.Integer)


class memberBankAccount(db.Model):
    __tablename__ = 'member_bank_account'
    id = db.Column(db.Integer, primary_key=True)
    account_type = db.Column(db.String(10), nullable=False)
    bank_name = db.Column(db.String(100), nullable=False)
    branch = db.Column(db.String(100), nullable=False)
    account_name = db.Column(db.String(100), nullable=False)
    account_number = db.Column(db.String(50), nullable=False)
    IFSC_code = db.Column(db.String(20), nullable=False)
    member_id = db.Column(db.Integer, db.ForeignKey('members.member_id'), nullable=False)
    
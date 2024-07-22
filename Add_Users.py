from application.models import Users
from application.database import db
from application.app import user_datastore
import datetime
from flask_security import hash_password

def create_users(): 
    if not user_datastore.find_user(email='admin@shgplus.in'):
        user_datastore.create_user(id=1, first_name='Admin', last_name='Admin', email='admin@shgplus.in', password=hash_password('password'),  last_login=datetime.datetime.now(), roles=['admin'], date_created=datetime.datetime.now())
    
    if not user_datastore.find_user(email='operator@shgplus.in'):
        user_datastore.create_user(id=2, first_name='Mayur', last_name='Kharade', email='operator@shgplus.in', password=hash_password('password'), last_login=datetime.datetime.now(), roles=['operator'], date_created=datetime.datetime.now())

    if not user_datastore.find_user(email='manager@shgplus.in'):
        user_datastore.create_user(id=3, first_name='Mayur', last_name='Kharade', email='manager@shgplus.in', password=hash_password('password'), last_login=datetime.datetime.now(), roles=['manager'], date_created=datetime.datetime.now())
     
    
    db.session.commit()
    print("Users created successfully!")

try:
    create_users()
except Exception as e:
    print(e)
    print("Users already created!")
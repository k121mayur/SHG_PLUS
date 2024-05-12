from application.models import Roles
from application.database import db
from application.app import user_datastore


def create_roles():
    user_datastore.find_or_create_role(name='admin', description='Admin role')
    user_datastore.find_or_create_role(name='operator', description='Data Entry Operator Access')
    user_datastore.find_or_create_role(name='manager', description='Mananger Access ')
    db.session.commit()
    print("Roles created successfully!")

# Function calling will create 4 roles as planned!
try:
    create_roles()
except:
    print("Roles already created!")
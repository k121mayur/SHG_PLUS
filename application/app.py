import os
from flask import Flask
from application.database import db
from flask_migrate import Migrate
from application.models import *
from flask_restful import Api
from flask_cors import CORS
from flask_security import Security, SQLAlchemyUserDatastore
# from application.worker import celery_init_app
# from application.instances import cache
from celery.schedules import crontab
# from application.tasks import daily_reminder

basedir = os.path.abspath(os.path.dirname(__file__))
tp = os.path.join(basedir, "../templates")
st = os.path.join(basedir, "../static")
app = Flask(__name__, template_folder=tp, static_folder=st)
CORS(app, supports_credentials=True)
CORS(app)
CORS(app, resources={r"/*": {"origins": "http://localhost:8080", "supports_credentials": True, "headers": "Content-Type, Token"}})
# CORS(app, resources={"/role": {"origins": "http://localhost:8080", "allow_headers": ["authentication-token", "Content-Type"]}})
# CORS(app, origins=["*"], allow_headers=["token", "Content-Type"])
# CORS(app, resources={r"/*": {"origins": "http://localhost:8080", "allow_headers": ["Authentication-Token", "Content-Type"]}})

api = Api(app)

migrate = Migrate(app, db)


SQLITE_DB_DIR = os.path.join(basedir, "../database")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(SQLITE_DB_DIR, "dev.sqlite3")
app.config["SECURITY_TOKEN_AUTHENTICATION_KEY"] = "1234567890"
app.config["SECURITY_TOKEN_AUTHENTICATION_HEADER"] = "Token"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECURITY_FRESHNESS_GRACE_PERIOD'] = 300
app.config['SECURITY_PASSWORD_SALT'] = 'salt'
app.config['SECURITY_TOKEN_URL_SAFE'] = True
app.config['SECURITY_TOKEN_AUTHENTICATION_SCHEME'] = 'Bearer'
app.config['SECRET_KEY'] = 'mayur' 
app.config['WTF_CSRF_ENABLED'] = False

user_datastore = SQLAlchemyUserDatastore(db, Users, Roles)
security = Security(app)
security.init_app(app, user_datastore)
db.init_app(app)

# celery_app = celery_init_app(app)
# cache.init_app(app)


# @celery_app.on_after_configure.connect
# def send_email(sender, **kwargs):
#     sender.add_periodic_task(
#         crontab(hour=3, minute=2),
#         daily_reminder.s('narendra@email.com', 'Daily Test'),
#     )



app.app_context().push()

from application.controllers import *

from application.api import *

# api.add_resource(userApi, "/api/v1/user", "/api/v1/user/<int:user_id>")
api.add_resource(shgApi, "/api/v1/shg", "/api/v1/shg/<int:shg_id>", "/api/v1/shgs/byMonth/<int:month>")
api.add_resource(memberApi, "/api/v1/member", "/api/v1/member/<int:shg_id>",  "/api/v1/meeting/member/<int:meeting_id>")
api.add_resource(meetingApi, "/api/v1/meeting", "/api/v1/meeting/<int:shg_id>")
api.add_resource(memberReceiptApi, "/api/v1/memberReceipt", "/api/v1/memberReceipts/<int:meeting_id>")
api.add_resource(shgBankAccountApi, "/api/v1/ShgAccount", "/api/v1/ShgAccount/<int:shg_id>", "/api/v1/ShgAccount/<int:shg_id>/<int:account_type>")
api.add_resource(otherLoanReceiptsApi, "/api/v1/otherLoanReceipts" , "/api/v1/otherLoanReceipts/<int:meeting_id>")
api.add_resource(otherSavingsReceiptsApi, "/api/v1/otherSavingsReceipts", "/api/v1/otherSavingsReceipts/<int:meeting_id>")
api.add_resource(loanPurposeListApi, "/api/v1/loanPurposeList")
api.add_resource(memberLoanPaymentsApi, "/api/v1/memberLoanPayments")
api.add_resource(memberSavingsPaymentsApi, "/api/v1/memberSavingsPayments")
api.add_resource(bankEmiPaymentsApi, "/api/v1/bankEmiPayments")
api.add_resource(savingsAccountPaymentsApi, "/api/v1/savingsAccountPayments")
api.add_resource(otherServiceChargePaymentsApi, "/api/v1/serviceChargePayments")
api.add_resource(otherCashInHandPaymentsApi, "/api/v1/cashInHandPayments")

api.add_resource(operatorDashboardApi, "/api/v1/operatorDashboard")
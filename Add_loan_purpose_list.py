from application.models import loanPurposeList
from application.database import db



def add_loan_purposes():
    raw_data = [
        ("01-A", "Dhan, Wheat, and Other Agriculture Seeds"),
        ("01-B", "Vegetable Cultivation"),
        ("01-C", "Livestock"),
        ("01-D", "Motor, Engine, and Others"),
        ("01-E", "Purchasing Land"),
        ("01-F", "Taking Land on Lease"),
        ("01-G", "Deepening the Well, Borewell, etc."),
        ("01-H", "Other Production Work"),
        ("02-A", "Children's Education"),
        ("02-B", "Health"),
        ("03-A", "Health of Livestock"),
        ("03-B", "Goat Rearing"),
        ("03-C", "Business"),
        ("03-D", "Poultry"),
        ("04-A", "Worshipping"),
        ("04-B", "Vehicle"),
        ("04-C", "Housing"),
        ("04-D", "T.V., Mixture Machine, and Others"),
        ("04-E", "Repaying Old Outside Loan"),
        ("04-F", "Festival and Enjoyment"),
        ("04-G", "Marriage, Funeral, etc."),
        ("04-H", "Shopping"),
        ("04-I", "Ration"),
        ("04-J", "Traveling"),
        ("04-K", "Case, Police, and Others"),
        ("04-L", "Purchasing Property"),
        ("04-M", "Other"),
    ]

    for code, purpose in raw_data:
        loan_purpose = purpose
        if not loanPurposeList.query.filter_by(loan_purpose=loan_purpose).first():
            new_purpose = loanPurposeList(loan_type_id=code, loan_purpose=loan_purpose)
            db.session.add(new_purpose)
    db.session.commit()

add_loan_purposes()
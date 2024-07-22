from application.models import schemes
from application.database import db


schemes_data = [
    "Ayushman Bharat",
    "Pradhan Mantri Jivan Jyoti Bima Yojana",
    "Pradhan Mantri Surksha Bima Yojana", 
    "Labour Card"
]

for scheme in schemes_data:
    if not schemes.query.filter_by(scheme_name=scheme).first():
        new_scheme = schemes(scheme_name=scheme)
        db.session.add(new_scheme)

db.session.commit()
print("Schemes added successfully")
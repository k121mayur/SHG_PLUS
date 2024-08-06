from application.database import db
from application.models import SHG, members, shgBankAccount
from datetime import datetime

check = db.session.query(SHG.shg_name == "TEST SHG").first()
check_1 = db.session.query(SHG.shg_name == "Mahakal SHG").first()

print(check)
print(check_1)


new_shg = SHG(
            shg_name="TEST SHG",
            project_name="project_name",
            village_name="Aundh",
            panchayat_name="Aundh",
            group_address="Near Hanuman Temple, Aundh, Tal-Khatav, Dist-Satara 41",
            formation_date= datetime.strptime("2024-01-01", "%Y-%m-%d").date(),
            first_saving_date= datetime.strptime("2024-01-01", "%Y-%m-%d").date(),
            total_no_of_members=15,
            saving_day=5,
            staff_name="Aditi Jha",
            samuh_sakhi_name="Komal Bund",
            per_share_size_in_INR="20"
        )

new_shg_1 = SHG(
            shg_name="Mahakal SHG",
            project_name="project_name",
            village_name="Vaduj",
            panchayat_name="Gopuj",
            group_address="Near Ram Temple, Gopuj, Tal-Khatav, Dist-Satara 41",
            formation_date= datetime.strptime("2024-03-01", "%Y-%m-%d").date(),
            first_saving_date= datetime.strptime("2024-01-01", "%Y-%m-%d").date(),
            total_no_of_members=17,
            saving_day=6,
            staff_name="Snehal Bhosale",
            samuh_sakhi_name="Savita Mali",
            per_share_size_in_INR="30"
        )


if check is None:
    db.session.add(new_shg)

if  check_1 is None:
    db.session.add(new_shg_1)
    


db.session.commit()


check = db.session.query(members.first_name == "Mayur").first()
check_1 = db.session.query(members.first_name == "Komal").first()


print(check)
print(check_1)

new_member = members(
            shg_id=1,  # Assuming `id` is the correct identifier
            village="Aundh",

            joining_date= datetime.today().date(),
            household_code="220",
            first_name="Mayur",
            father_husband_name="Jaywant",
            last_name="Kharade",
            number_of_family_members=5,
            voter_id="",
            adhar_id="",
            pan_number="HBRPK9155H",
            ration_card_number="",
            education="Primary",
            category= "General",  # Convert list to comma-separated string
            caste="Yadav",
            mobile_number="9503633030",
            total_land_kattha=3,
            total_irrigated_land_kattha=2,
            total_no_of_goats=5,
            total_no_of_cattle=4,
            total_no_of_members_migrated=4,
            main_source_of_income="Agri",
            head_of_the_family_name="Mayur Kharade",
        )


new_member_1 = members(
            shg_id=1,  # Assuming `id` is the correct identifier
            village="Aundh",
            joining_date= datetime.today().date(),
            household_code="220",
            first_name="Komal",
            father_husband_name="Vilas",
            last_name="Sardar",
            number_of_family_members=5,
            voter_id="",
            adhar_id="",
            pan_number="HBRPK9155E",
            ration_card_number="",
            education="Primary",
            category= "General",  # Convert list to comma-separated string
            caste="Yadav",
            mobile_number="9503633029",
            total_land_kattha=3,
            total_irrigated_land_kattha=2,
            total_no_of_goats=5,
            total_no_of_cattle=4,
            total_no_of_members_migrated=4,
            main_source_of_income="Agri",
            head_of_the_family_name="Mayur Kharade",
        )


if check is None:
    db.session.add(new_member)

if  check_1 is None:
    db.session.add(new_member_1)
    
db.session.commit()


loan_account_check = db.session.query(shgBankAccount.account_number == "0012229384755").first()
saving_account_check = db.session.query(shgBankAccount.account_number == "00122293847551").first()

print(loan_account_check)
print(saving_account_check)

shg_loan_account = shgBankAccount(
    id = 1,
    account_type = "loan",
    bank_name = "HDFC Bank",
    branch = "Gaya",
    account_name = "TEST SHG",
    account_number = "0012229384755",
    IFSC_code = "HDFC0000012",
    shg_id = 1,
    balance = 100000
)


shg_saving_account = shgBankAccount(
    id = 2,
    account_type = "savings",
    bank_name = "HDFC Bank",
    branch = "Gaya",
    account_name = "TEST SHG",
    account_number = "00122293847551",
    IFSC_code = "HDFC0000012",
    shg_id = 1,
    balance = 100000
)

if loan_account_check is None:
    db.session.add(shg_loan_account)
    print("loan account added")
    db.session.commit()

if saving_account_check is None:
    db.session.add(shg_saving_account)
    print("Savings account added")
    db.session.commit()

print("Done!")
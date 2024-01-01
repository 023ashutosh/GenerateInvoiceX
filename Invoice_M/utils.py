from faker import Faker
from Invoice_M import app,db
from Invoice_M.models import UserRegistration

# fake = Faker('en_IN')

# def generate_dummy_data():
#     with db.app.app_context():
#         # Create 100 dummy users
#         for _ in range(100):
#             user = UserRegistration(
#                 First_name=fake.first_name(),
#                 Last_name=fake.last_name(),
#                 Username=fake.user_name(),
#                 Email=fake.email(),
#                 Phone_No=fake.random_int(min=1000000000, max=9999999999),
#                 Password=fake.password(),
#                 image_file='default.jpg',
#                 Department='Start-Up',
#                 Post=fake.job(),
#                 Salary=fake.random_int(min=30000, max=100000),
#                 Location=fake.city()
#             )
#             db.session.add(user)

#         # Commit the changes to the database
#         db.session.commit()



def get_next_emp_id():
    # Check the last used Emp_id in the database
    last_user = UserRegistration.query.order_by(UserRegistration.Emp_id.desc()).first()

    if last_user:
        # If there are existing users, increment the last Emp_id
        next_emp_id = last_user.Emp_id + 1
    else:
        # If there are no existing users, start from 10001
        next_emp_id = 10001

    return next_emp_id


# def validate_date_format(form, DateField):
#         try:
#             datetime.strptime(DateField.data, '%d/%m/%Y')
#         except ValueError:
#             raise ValidationError('Invalid date format. Please use DD/MM/YYYY.')
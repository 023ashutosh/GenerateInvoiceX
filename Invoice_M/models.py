from Invoice_M import db, login_manager
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
   return UserRegistration.query.filter_by(Email=user_id).first()


class WorkingDays(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   month = db.Column(db.Integer, nullable=False)
   year = db.Column(db.Integer, nullable=False)
   working_days = db.Column(db.Integer, nullable=False)
   def __repr__(self):
      return f"WorkingDays('{self.month}', '{self.year}', '{self.working_days}')"


class UserRegistration(db.Model, UserMixin):
   
   # PERSONAL DETAILS
   Emp_id = db.Column(db.Integer(), primary_key = True )
   First_name = db.Column(db.String(20), unique = False, nullable = False)
   Last_name = db.Column(db.String(20), unique = False, nullable = False)
   Username = db.Column(db.String(20), unique = True, nullable = False)
   Email = db.Column(db.String(120), unique = True, nullable = False)
   Phone_No = db.Column(db.Integer(), unique = True, nullable = False)
   image_file = db.Column(db.String(20), nullable = False, default = 'default.jpg')
   Password = db.Column(db.String(60), nullable = False) 
   # EMPLOYMENT DETAILS
   Department = db.Column(db.String(50), nullable=False)
   Post = db.Column(db.String(120), unique = False, nullable = False)
   # Date_Joining = db.Column(db.Date(), nullable=False, default=datetime.utcnow)
   Salary = db.Column(db.Integer(), unique=False, nullable=False)
   Location = db.Column(db.String(30), nullable=False)
   def __repr__(self):
      return f"UserRegistration('{self.Emp_id}', '{self.First_name}', '{self.Last_name}', '{self.Username}', '{self.Email}', '{self.Phone_No}', '{self.Department}', '{self.Post}', '{self.Salary}', '{self.Location}')"
   
   def get_id(self):
      return str(self.Email)
   
# For terminal

# python
# from Invoice_M import app,db
# from Invoice_M.models import UserRegistration
# app.app_context().push()
# user = UserRegistration.query.first()
# user.password

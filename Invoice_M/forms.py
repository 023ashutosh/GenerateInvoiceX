from collections.abc import Mapping, Sequence
from typing import Any
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, BooleanField, PasswordField, SubmitField, DateField, SelectField, validators
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from Invoice_M.models import UserRegistration
# from datetime import datetime
# from Invoice_M.utils import validate_date_format



# app.config['SECRET_KEY'] = 'qwertyuiop'


class NewLogin(FlaskForm):

    # PERSONAL DETAILS
    Emp_id = IntegerField('Employee Id')
    
    First_name = StringField('First Name', validators=[DataRequired()])
    
    Last_name = StringField('Last Name', validators=[DataRequired()])

    Username = StringField('Username', validators=[DataRequired()])
    
    Email = StringField('Email id', validators=[DataRequired(), Email()])
    
    Phone_No = StringField('Phone', validators=[DataRequired(), Length(min=10, max=10)])
    
    Password = PasswordField('Password', validators=[DataRequired()])
    
    Confirm_Password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('Password')])


    # EMPLOYMENT DETAILS
    Department = StringField('Department', validators=[DataRequired()])

    post_choices = [
        ('Employee'),
        ('Software Developer'),
        ('Sales Executive'),
        ('Graphic Designer'),
        ('Owner'),
        ('Manager'),
     ]
    
    Post = SelectField('Post', choices=post_choices, validators=[DataRequired()])
    
    # Date_Joining = DateField('Date Joining (DD/MM/YYYY)', format='%d/%m/%Y', validators=[DataRequired(), validate_date_format])
    
    Salary = StringField('Salary', validators=[DataRequired()])  
    
    Location = StringField('Location', validators=[DataRequired()])



    submit = SubmitField('ADD')

    def validate_Emp_id(self, Emp_id):

        user = UserRegistration.query.filter_by(Emp_id=Emp_id.data).first()
        if user:
            raise ValidationError('The Employee Id is already taken.')

    def validate_Username(self, Username):

        user = UserRegistration.query.filter_by(Username=Username.data).first()
        if user:
            raise ValidationError('The Username is already taken.')
        
    def validate_Email(self, Email):

        user = UserRegistration.query.filter_by(Email=Email.data).first()
        if user:
            raise ValidationError('The Email is already taken.')
    
    def validate_Phone_No(self, Phone_No):

        user = UserRegistration.query.filter_by(Phone_No=Phone_No.data).first()
        if user:
            raise ValidationError('The Phone No is already taken.')
        





class UpdateForm(FlaskForm):

        Email = StringField('Email id', validators=[DataRequired(), Email()])

        # PERSONAL DETAILS
        
        Username = StringField('Username', validators=[DataRequired()])
        
        Phone_No = StringField('Phone', validators=[DataRequired(), Length(min=10, max=10)])

        # EMPLOYMENT DETAILS
        Department = StringField('Department', validators=[DataRequired()])

        post_choices = [
            ('employee', 'Employee'),
            ('software_developer', 'Software Developer'),
            ('sales_executive', 'Sales Executive'),
            ('graphic_designer', 'Graphic Designer'),
        ]
        
        Post = SelectField('Post', choices=post_choices, validators=[DataRequired()])
        
        # Date_Joining = DateField('Date Joining (DD/MM/YYYY)', format='%d/%m/%Y', validators=[DataRequired(), validate_date_format])
        
        Salary = StringField('Salary', validators=[DataRequired()])  
        
        Location = StringField('Location', validators=[DataRequired()])

        submit = SubmitField('UPDATE')

        
        
            
        
        
class LoginForm(FlaskForm):
    Email = StringField('Email id', validators=[DataRequired(), Email()])
    
    Password = PasswordField('Password', validators=[DataRequired()])


    
    submit = SubmitField('LOGIN')







class WorkingDaysForm(FlaskForm):
    working_days = IntegerField('Working Days', validators=[DataRequired()])
    submit = SubmitField('Submit')

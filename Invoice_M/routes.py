from flask import render_template, request, url_for, flash, redirect
from Invoice_M import app, db, bcrypt
from Invoice_M.forms import NewLogin, LoginForm, UpdateForm, WorkingDaysForm
from Invoice_M.models import UserRegistration, WorkingDays
from flask_login import login_user, current_user, logout_user, login_required
from Invoice_M.utils import get_next_emp_id
from datetime import datetime


# TEST ROUTING
# Test Route 1
@app.route("/test1")
def test1():
    return render_template("test1.html") 


# Test Route 2
@app.route("/test2")
def test2():
    return render_template("test2.html")


# MAIN ROUTING


# Home Page Route
# /
@app.route("/")
def home():
    total_users = UserRegistration.query.count()
    latest_entry = WorkingDays.query.order_by(WorkingDays.id.desc()).first()
    current_working_days = latest_entry.working_days if latest_entry else 0
    today_date = datetime.now().strftime("%d %b, %Y")
    users = UserRegistration.query.all()
    total_salary = sum(
        int(user.Salary.replace('Rs. ', '').replace(',', '')) if isinstance(user.Salary, str) else int(user.Salary)
        for user in users
    )
    return render_template("index.html", total_users = total_users, current_working_days = current_working_days, today_date = today_date, total_salary = total_salary, users=users)


# Attendance Page Route
# /attendance
@app.route("/attendance")
@login_required
def attendance():
    return render_template("attendance.html")


# Attendance Page Route
# /attendance/new_login
@app.route("/attendance/new_login", methods=['GET','POST'])
@login_required
def new_login():
    form = NewLogin()
    emp_id = get_next_emp_id()

    # if current_user.is_authenticated:
        # return redirect(url_for('home'))
    
    if form.validate_on_submit():
        
        hashed_password = bcrypt.generate_password_hash(form.Confirm_Password.data).decode('utf-8')
        
        user = UserRegistration(Emp_id=emp_id, First_name=form.First_name.data, Last_name=form.Last_name.data, Username=form.Username.data, Email=form.Email.data, Phone_No=form.Phone_No.data, Password=hashed_password, Department=form.Department.data, Post=form.Post.data, Salary=form.Salary.data, Location=form.Location.data)
    
        # app.app_context.push()
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created and now you are able to Login.', 'success')
        return redirect(url_for('login'))
    
    form.Emp_id.render_kw = {'readonly': True}
    return render_template("/attendance/new_login.html", title = 'Invoice-New Login',  form = form, emp_id = emp_id)


# Attendance Page Route
# /attendance/view
@app.route("/attendance/view", methods=['GET'])
@login_required
def view():
    # app.app_context().push()
    users = UserRegistration.query.all()
    return render_template("/attendance/view.html", users=users)







@app.route("/attendance/modify", methods=['GET', 'POST'])
@login_required
def modify():
    form = UpdateForm()

    # Handle the GET request to display the search form
    if request.method == 'GET':
        email_to_search = request.args.get('emailSearch')
        print(f"Email to Search: {email_to_search}")

        if email_to_search:
            # If an email is provided, query the user based on the email
            user_to_modify = UserRegistration.query.filter_by(Email=email_to_search).first()
            print(f"User to modify: {user_to_modify}")

            if user_to_modify:
                # If user found, render the form with user details
                flash('Employee found. You can modify the details below.', 'info')
                return render_template("/attendance/modify.html", form=form, user_to_modify=user_to_modify)

            else:
                flash('Employee not found in the Employee records', 'danger')

    # Handle the POST request to update the user information
    elif request.method == 'POST':
        # form = UpdateForm(request.form)

        if form.validate_on_submit():
            email_to_modify = form.Email.data
            user_to_modify = UserRegistration.query.filter_by(Email=email_to_modify).first()

            if user_to_modify:
                # Update the existing entry based on the form data
                user_to_modify.Username = form.Username.data
                user_to_modify.Phone_No = form.Phone_No.data
                user_to_modify.Department = form.Department.data
                user_to_modify.Post = form.Post.data
                user_to_modify.Salary = form.Salary.data
                user_to_modify.Location = form.Location.data

                db.session.commit()
                
                flash('User information updated successfully', 'success')
                return redirect(url_for('home'))
                
            else:
                flash('Unable to update in the Employee records', 'danger')
                


        else:
            flash('Form validation failed. Please check your input.', 'danger')
           
    return render_template("/attendance/modify.html", form=form, user_to_modify=None )




# Attendance Page Route     
# /attendance/delete
@app.route("/attendance/delete", methods=['GET', 'POST'])
@login_required
def delete():
    form = UpdateForm()

    # Handle the GET request to display the search form
    if request.method == 'GET':
        email_to_search = request.args.get('EmailSearch')
        print(f"Email to Search: {email_to_search}")

        if email_to_search:
            # If an email is provided, query the user based on the email
            user_to_delete = UserRegistration.query.filter_by(Email=email_to_search).first()
            print(f"User to delete: {user_to_delete}")

            if user_to_delete:
                # If user found, render the form with user details and confirmation prompt
                flash('Employee found. Do you want to delete this entry?', 'info')
                return render_template("/attendance/delete.html", form=form, user_to_delete=user_to_delete)

            else:
                flash('Employee not found in the Employee records', 'danger')

    # Handle the POST request to delete the user
    elif request.method == 'POST':
        email_to_delete = form.Email.data
        user_to_delete = UserRegistration.query.filter_by(Email=email_to_delete).first()

        if user_to_delete:
            # Delete the user from the database
            db.session.delete(user_to_delete)
            db.session.commit()

            flash('User information deleted successfully', 'success')
            return redirect(url_for('home'))

        else:
            flash('Unable to delete. Employee not found in the records', 'danger')

    return render_template("/attendance/delete.html", form=form, user_to_delete=None)



# /working_days
@app.route("/working_days", methods=['GET', 'POST'])
@login_required
def working_days():
    form = WorkingDaysForm()

    if form.validate_on_submit():
        month = datetime.now().month
        year = datetime.now().year
        working_days_value = form.working_days.data

        # Save the data to the database
        working_days_entry = WorkingDays(month=month, year=year, working_days=working_days_value)
        db.session.add(working_days_entry)
        db.session.commit()

        flash('Working days updated successfully!', 'success')
        return redirect(url_for('home'))

    return render_template("working_days.html", form=form)






# Main Route 2 
# Attendance Page Route
# /invoice
@app.route("/invoice")
@login_required
def invoice():
    return render_template("invoice.html")






#attendance login route
@app.route("/login", methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = UserRegistration.query.filter_by(Email = form.Email.data).first()
        if user and bcrypt.check_password_hash(user.Password, form.Password.data):
            login_user(user, remember = False)
            flash(f'Login successful.', 'success')
            return redirect(url_for('home'))
    # else:
    #     flash(f'Login unsucessful. Please check Email and Password.', 'danger')
    return render_template("login.html", title = 'Login', form = form)



@app.route("/account")
@login_required
def account():
    image_file = url_for('static', filename = 'profile_pics/'+current_user.image_file)
    return render_template("account.html", title = 'Account', image_file=image_file)




#attendance logout route
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash(f'Logout successful.', 'warning')
    return redirect(url_for('home'))

    

